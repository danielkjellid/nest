import pytest

from nest.exceptions import ApplicationError
from nest.selectors import UserSelector
from nest.tests.utilities import create_user

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
        raise AssertionError()
