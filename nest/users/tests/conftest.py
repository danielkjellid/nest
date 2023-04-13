import pytest
from django.contrib.auth.models import AnonymousUser, Permission

TEST_PASSWORD = "supersecretpassword"

###############
# Permissions #
###############


@pytest.fixture
def test_permissions(request):
    try:
        return [request.param]
    except AttributeError:
        return []


#########
# Users #
#########


@pytest.fixture
def create_user_with_permissions(django_user_model):
    """
    Returns a factory creating users given permissions.
    """

    def _make_user(perms, email="testuser@example.com", **defaults):
        user = django_user_model.objects.update_or_create(
            email=email,
            **defaults,
        )[0]
        user.set_password(TEST_PASSWORD)

        parsed_perms: list[Permission] = []

        for perm in perms:
            parsed_perm = Permission.objects.filter(codename=perm)

            # If multiple codenames are found, add them all.
            if len(parsed_perm) > 1:
                parsed_perm = list(parsed_perm)  # type: ignore
                parsed_perms.extend(parsed_perm)
            else:
                parsed_perms.append(parsed_perm[0])

        user.user_permissions.set(parsed_perms)
        user.save()

        return user

    return _make_user


@pytest.fixture
def anonymous_user_fixture():
    return AnonymousUser()


@pytest.fixture
def user_fixture(create_user_with_permissions, test_permissions):
    return create_user_with_permissions(
        test_permissions,
        first_name="User",
        last_name="Fixture",
        email="user@example.com",
    )


@pytest.fixture
def staff_user_fixture(create_user_with_permissions, test_permissions):
    return create_user_with_permissions(
        test_permissions,
        first_name="Staff User",
        last_name="Fixture",
        email="staff_user@example.com",
        is_staff=True,
    )


@pytest.fixture
def superuser_fixture(create_user_with_permissions):
    return create_user_with_permissions(
        [],
        first_name="Super User",
        last_name="Fixture",
        email="superuser@example.com",
        is_superuser=True,
        is_staff=True,
    )
