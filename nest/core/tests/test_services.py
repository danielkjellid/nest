import pytest

from nest.audit_logs.models import LogEntry
from nest.core.services import model_update
from nest.homes.tests.utils import create_home
from nest.users.core.tests.utils import create_user

pytestmark = pytest.mark.django_db


class TestCoreServices:
    def test_model_update_does_nothing(self, django_assert_num_queries):
        """
        Test that the model_update service does not perform any updates when no fields
        are provided, or no fields are present in data.
        """
        user = create_user()

        # When fields are empty, it should not do anything.
        with django_assert_num_queries(0):
            updated_user1, has_updated1 = model_update(instance=user, data={})

        assert user == updated_user1
        assert has_updated1 is False

        # When none of the fields specified in fields are present in data, it should
        # not do anything.
        with django_assert_num_queries(0):
            updated_user2, has_updated2 = model_update(
                instance=user, data={"foo": "bar"}
            )

        assert user == updated_user2
        assert has_updated2 is False

    def test_model_update_updates_only_passed_fields_from_data(
        self, django_assert_num_queries
    ):
        """
        Test that the model_update service only updates data related to the fields
        defined. E.g. even though the data parameter contains multiple fields,
        it should only update the fields specified.
        """

        user = create_user(first_name="Tony", last_name="Montana", is_superuser=False)

        ignore_fields = ["last_name"]
        data = {"first_name": "Anthony", "last_name": "Scarface", "is_superuser": True}

        assert user.first_name != data["first_name"]

        with django_assert_num_queries(4):
            updated_user, has_updated = model_update(
                instance=user, ignore_fields=ignore_fields, data=data
            )

        assert has_updated is True
        assert updated_user.first_name == data["first_name"]
        assert user.last_name == updated_user.last_name
        assert user.is_superuser == updated_user.is_superuser

    def test_model_update_updates_many_to_many_field(self, django_assert_num_queries):
        """
        Test that the model_update service correctly updates m2m fields where
        applicable.
        """

        home1 = create_home(street_address="Address 1")
        home2 = create_home(street_address="Address 2")
        home3 = create_home(street_address="Address 3")
        user = create_user(homes=[home1, home2])

        data = {"homes": [home3]}

        assert home3 not in user.homes.all()

        original_updated_at = user.updated_at

        with django_assert_num_queries(3):
            updated_user, has_updated = model_update(instance=user, data=data)

        assert user == updated_user
        assert has_updated is True
        assert home3 in updated_user.homes.all()
        assert [home1, home2] not in updated_user.homes.all()

        # Updating only m2m should not bump updated at.
        assert original_updated_at == updated_user.updated_at

    def test_model_update_standard_and_many_to_many_fields(
        self, django_assert_num_queries
    ):
        """
        Test that the model_update service correctly updates both standard fields and
        m2m fields when both passed as the same time.
        """
        home1 = create_home(street_address="Address 1")
        home2 = create_home(street_address="Address 2")

        user = create_user(first_name="Homer", last_name="Simpson", homes=[home1])

        data = {"first_name": "Bart", "homes": [home2]}

        with django_assert_num_queries(7):
            updated_user, has_updated = model_update(instance=user, data=data)

        assert has_updated is True
        assert updated_user.first_name == data["first_name"]
        assert home2 in updated_user.homes.all()
        assert home1 not in updated_user.homes.all()

    def test_model_update_creates_log_entry_by_default(self, django_assert_num_queries):
        """
        Test that the model_update service creates a log entry by default when
        performing updates.
        """

        user = create_user(first_name="Peter", last_name="Griffin")
        data = {"first_name": "Brian"}

        assert LogEntry.objects.count() == 0

        with django_assert_num_queries(4):
            updated_user, has_updated = model_update(instance=user, data=data)

        assert has_updated is True
        assert updated_user.first_name == data["first_name"]
        assert updated_user.last_name == user.last_name
        assert LogEntry.objects.count() == 1
        assert LogEntry.objects.first().object_id == updated_user.id

    def test_model_update_does_not_create_log_entry_when_specified(
        self, django_assert_num_queries
    ):
        """
        Test that the model_update service does not create a log entry when explicitly
        turned off.
        """

        user = create_user(first_name="Peter", last_name="Griffin")
        data = {"first_name": "Brian"}

        assert LogEntry.objects.count() == 0

        with django_assert_num_queries(3):
            _updated_user, has_updated = model_update(
                instance=user, data=data, log_change=False
            )

        assert has_updated is True
        assert LogEntry.objects.count() == 0
