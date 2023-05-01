import pytest
from django.test.client import RequestFactory

from nest.frontend.records import (
    FrontendMenuItemRecord,
    FrontendInitialPropsRecord,
    FrontendConfigRecord,
)
from nest.frontend.selectors import get_initial_props, get_menu_for_user
from nest.homes.records import HomeRecord
from nest.homes.tests.utils import create_home
from nest.users.records import UserRecord
from nest.users.tests.utils import create_user

pytestmark = pytest.mark.django_db


class TestFrontendSelectors:
    def test_get_initial_props(self, django_assert_num_queries, settings):
        """
        Test that the initial props selector returns expected output within query
        limits.
        """
        settings.IS_PRODUCTION = True

        home = create_home()
        user = create_user(home=home)

        request = RequestFactory()
        request.user = user

        with django_assert_num_queries(1):
            initial_props = get_initial_props(request=request)

        assert initial_props == FrontendInitialPropsRecord(
            menu=[
                FrontendMenuItemRecord(key="plans", title="Meal plans", end=True),
                FrontendMenuItemRecord(key="products", title="Products", end=True),
                FrontendMenuItemRecord(key="recipes", title="Recipes", end=True),
                FrontendMenuItemRecord(key="settings", title="Settings", end=True),
            ],
            config=FrontendConfigRecord(is_production=True),
            current_user=UserRecord.from_user(user),
            available_homes=[HomeRecord.from_home(home)],
        )

    def test_user_menu(self, django_assert_num_queries):
        """
        Test that the user menu selector returns expected output within query
        limits.
        """

        user = create_user(is_staff=False)
        expected_non_staff_output = [
            FrontendMenuItemRecord(key="plans", title="Meal plans", end=True),
            FrontendMenuItemRecord(key="products", title="Products", end=True),
            FrontendMenuItemRecord(key="recipes", title="Recipes", end=True),
            FrontendMenuItemRecord(key="settings", title="Settings", end=True),
        ]

        with django_assert_num_queries(0):
            non_staff_output = get_menu_for_user(user=UserRecord.from_user(user))

        assert non_staff_output == expected_non_staff_output

        staff_user = create_user(is_staff=True)
        expected_staff_output = [
            FrontendMenuItemRecord(key="plans", title="Meal plans", end=True),
            FrontendMenuItemRecord(key="products", title="Products", end=True),
            FrontendMenuItemRecord(key="recipes", title="Recipes", end=True),
            FrontendMenuItemRecord(key="settings", title="Settings", end=True),
            FrontendMenuItemRecord(key="users", title="Users", end=True),
        ]

        with django_assert_num_queries(0):
            staff_output = get_menu_for_user(user=UserRecord.from_user(staff_user))

        assert staff_output == expected_staff_output
