import pytest
from django.test.client import RequestFactory

from nest.records import (
    CoreConfigRecord,
    CoreInitialPropsRecord,
    CoreMenuItemRecord,
    HomeRecord,
    UserRecord,
)
from nest.selectors import CoreSelector
from nest.tests.utilities import create_home, create_user

pytestmark = pytest.mark.django_db


class TestCoreSelector:
    def test_initial_props(self, django_assert_num_queries, settings):
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
            initial_props = CoreSelector.initial_props(request=request)

        assert initial_props == CoreInitialPropsRecord(
            menu=[
                CoreMenuItemRecord(key="plans", title="Meal plans", end=True),
                CoreMenuItemRecord(key="products", title="Products", end=True),
                CoreMenuItemRecord(key="recipes", title="Recipes", end=True),
                CoreMenuItemRecord(key="settings", title="Settings", end=True),
            ],
            config=CoreConfigRecord(is_production=True),
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
            CoreMenuItemRecord(key="plans", title="Meal plans", end=True),
            CoreMenuItemRecord(key="products", title="Products", end=True),
            CoreMenuItemRecord(key="recipes", title="Recipes", end=True),
            CoreMenuItemRecord(key="settings", title="Settings", end=True),
        ]

        with django_assert_num_queries(0):
            non_staff_output = CoreSelector.user_menu(user=UserRecord.from_user(user))

        assert non_staff_output == expected_non_staff_output

        staff_user = create_user(is_staff=True)
        expected_staff_output = [
            CoreMenuItemRecord(key="plans", title="Meal plans", end=True),
            CoreMenuItemRecord(key="products", title="Products", end=True),
            CoreMenuItemRecord(key="recipes", title="Recipes", end=True),
            CoreMenuItemRecord(key="settings", title="Settings", end=True),
            CoreMenuItemRecord(key="users", title="Users", end=True),
        ]

        with django_assert_num_queries(0):
            staff_output = CoreSelector.user_menu(user=UserRecord.from_user(staff_user))

        assert staff_output == expected_staff_output
