import pytest

from nest.records import HomeRecord, UserRecord
from nest.selectors import HomeSelector
from nest.tests.utilities import create_home, create_user

pytestmark = pytest.mark.django_db


class TestHomeSelector:
    def test_all_homes(self, django_assert_num_queries):
        """
        Test that the all_homes selector returns expected output within query limits.
        """
        home1 = create_home(street_address="Address 1")
        home2 = create_home(street_address="Address 2")
        home3 = create_home(street_address="Address 3")

        expected_output = [
            HomeRecord.from_home(home1),
            HomeRecord.from_home(home2),
            HomeRecord.from_home(home3),
        ]

        with django_assert_num_queries(1):
            output = HomeSelector.all_homes()

        assert output == expected_output

    def test_user_homes(self, mocker, django_assert_num_queries):
        """
        Test that the user_homes selector returns expected output within query limits.
        """
        all_homes_selector_mock = mocker.patch(
            "nest.selectors.homes.HomeSelector.all_homes"
        )

        home1 = create_home(street_address="Address 1")
        home2 = create_home(street_address="Address 2")
        home3 = create_home(street_address="Address 3")

        staff_user = UserRecord.from_user(
            create_user(is_staff=True, home=home3, homes=[home1])
        )

        HomeSelector.user_homes(user=staff_user)
        assert all_homes_selector_mock.call_count == 1

        user = UserRecord.from_user(
            create_user(is_staff=False, home=home1, homes=[home2, home3])
        )
        with django_assert_num_queries(1):
            output = HomeSelector.user_homes(user=user)

        # Call count should not have been increased.
        assert all_homes_selector_mock.call_count == 1
        assert len(output) == 3
