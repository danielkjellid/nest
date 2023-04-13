import pytest

from nest.core.exceptions import ApplicationError
from nest.users.selectors import UserSelector
from nest.users.tests.utils import create_user
from nest.homes.tests.utils import create_home

pytestmark = pytest.mark.django_db


class TestUserSelector:
    def test_get_user(self, django_assert_num_queries):
        """
        Test that the get_user selector correctly gets the user and that it raises
        ApplicationError if the user does not exist.
        """
        user = create_user()

        with django_assert_num_queries(1):
            gotten_user = UserSelector.get_user(pk=user.id)

        assert user.id == gotten_user.id

        with pytest.raises(ApplicationError):
            UserSelector.get_user(pk=999)

    def test_all_users(self, django_assert_num_queries):
        """
        Test that the all_users selector correctly retrieves all users in the app within
        query limits.
        """
        create_user(first_name="User 1", home=create_home(street_address="Address 1"))
        create_user(first_name="User 2", home=create_home(street_address="Address 2"))
        create_user(first_name="User 3", home=create_home(street_address="Address 3"))

        with django_assert_num_queries(1):
            users = UserSelector.all_users()

        assert len(users) == 3
