import pytest

from nest.core.exceptions import ApplicationError
from nest.homes.tests.utils import create_home
from nest.users.selectors import get_user, get_users
from nest.users.tests.utils import create_user

pytestmark = pytest.mark.django_db


class TestUsersSelectors:
    def test_get_user(self, django_assert_num_queries):
        """
        Test that the get_user selector correctly gets the user and that it raises
        ApplicationError if the user does not exist.
        """
        user = create_user()

        with django_assert_num_queries(1):
            gotten_user = get_user(pk=user.id)

        assert user.id == gotten_user.id

        with pytest.raises(ApplicationError):
            get_user(pk=999)

    def test_get_users(self, django_assert_num_queries):
        """
        Test that the all_users selector correctly retrieves all users in the app within
        query limits.
        """
        create_user(first_name="User 1", home=create_home(street_address="Address 1"))
        create_user(first_name="User 2", home=create_home(street_address="Address 2"))
        create_user(first_name="User 3", home=create_home(street_address="Address 3"))

        with django_assert_num_queries(1):
            users = get_users()

        assert len(users) == 3
