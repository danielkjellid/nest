import pytest

from nest.core.exceptions import ApplicationError
from nest.users.models import User
from nest.users.services import create_user

pytestmark = pytest.mark.django_db


class TestUsersServices:
    def test_user_create(self, django_assert_num_queries, user_fixture) -> None:
        """
        Test that the "create" service creates a user.
        """
        with django_assert_num_queries(2):
            new_user = create_user(
                email="test@example.com",
                password="supersecret",
                is_active=True,
                first_name="Test",
                last_name="Example",
            )

        assert new_user.email == "test@example.com"
        assert new_user.is_active is True
        assert new_user.first_name == "Test"
        assert new_user.last_name == "Example"

        # Test that the password set is saved correctly.
        user = User.objects.get(id=new_user.id)
        assert user.check_password("supersecret") is True

        with pytest.raises(ApplicationError):
            # Test no provided email
            create_user(
                email="",
                password="supersecret",
                is_active=True,
            )

        with pytest.raises(ApplicationError):
            # Test user already exists
            existing_user = user_fixture
            create_user(
                email=existing_user.email,
                password="supersecret",
                is_active=True,
            )

        with pytest.raises(ApplicationError):
            # Test email does not pass validation.
            create_user(
                email="willnotpass",
                password="supersecret",
                is_active=True,
            )

        with pytest.raises(ApplicationError):
            # Test password does not pass validation.
            create_user(
                email="someone@example.com",
                password="1234",
                is_active=True,
            )
