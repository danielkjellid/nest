from django.contrib.auth.models import AnonymousUser

from nest.users.core.models import User

TEST_USER_PASSWORD = "supersecretpassword"


def create_user(email: str = "testuser@example.com", **defaults) -> User:
    user, _created = User.objects.update_or_create(email=email, **defaults)

    user.set_password(TEST_USER_PASSWORD)
    user.save()

    return user


def anonymous_user() -> AnonymousUser:
    return AnonymousUser()


def user() -> User:
    return create_user(first_name="User", last_name="Example", email="user@example.com")


def staff_user() -> User:
    return create_user(
        first_name="Staff User",
        last_name="Example",
        email="staff_user@example.com",
        is_staff=True,
    )


def superuser() -> User:
    return create_user(
        first_name="Super User",
        last_name="Example",
        email="superuser@example.com",
        is_staff=True,
        is_superuser=True,
    )
