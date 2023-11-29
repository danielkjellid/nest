import pytest

from nest.homes.records import HomeRecord
from nest.homes.selectors import get_homes, get_homes_for_user
from nest.homes.tests.utils import create_home
from nest.users.core.tests.utils import create_user
from nest.users.core.types import User

pytestmark = pytest.mark.django_db


class TestHomesSelectors:
    def test_get_homes(self, django_assert_num_queries):
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
            output = get_homes()

        assert output == expected_output

    def test_get_homes_for_user(self, mocker, django_assert_num_queries):
        """
        Test that the user_homes selector returns expected output within query limits.
        """
        all_homes_selector_mock = mocker.patch(
            f"{get_homes.__module__}.{get_homes.__name__}"
        )

        home1 = create_home(street_address="Address 1")
        home2 = create_home(street_address="Address 2")
        home3 = create_home(street_address="Address 3")

        staff_user = User.from_user(
            create_user(is_staff=True, home=home3, homes=[home1])
        )

        get_homes_for_user(user=staff_user)
        assert all_homes_selector_mock.call_count == 1

        user = User.from_user(
            create_user(is_staff=False, home=home1, homes=[home2, home3])
        )
        with django_assert_num_queries(1):
            output = get_homes_for_user(user=user)

        # Call count should not have been increased.
        assert all_homes_selector_mock.call_count == 1
        assert len(output) == 3
