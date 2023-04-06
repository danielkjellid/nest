import pytest
from django.contrib.auth.models import AnonymousUser, Permission
from django.test import Client

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
def anonymous_user():
    return AnonymousUser()


@pytest.fixture
def unprivileged_user(create_user_with_permissions):
    return create_user_with_permissions(
        [],
        first_name="Unprivileged",
        last_name="User",
        email="unprivileged_user@example.com",
    )


@pytest.fixture
def unprivileged_staff_user(create_user_with_permissions):
    return create_user_with_permissions(
        [],
        first_name="Unprivileged Staff",
        last_name="User",
        email="unprivileged_staff_user@example.com",
        is_staff=True,
    )


@pytest.fixture
def privileged_user(create_user_with_permissions, test_permissions):
    return create_user_with_permissions(
        test_permissions,
        first_name="Privileged",
        last_name="User",
        email="privileged_user@example.com",
    )


@pytest.fixture
def privileged_staff_user(create_user_with_permissions, test_permissions):

    return create_user_with_permissions(
        test_permissions,
        first_name="Privileged Staff",
        last_name="User",
        email="privileged_staff_user@example.com",
        is_staff=True,
    )


@pytest.fixture
def superuser(create_user_with_permissions):
    return create_user_with_permissions(
        [],
        first_name="Super",
        last_name="User",
        email="superuser@example.com",
        is_superuser=True,
        is_staff=True,
    )


@pytest.fixture
def anonymous_client_fixture():
    return Client()


@pytest.fixture
def authenticated_client(privileged_user):
    client = Client()
    client.login(username=unprivileged_user.email, password=TEST_PASSWORD)
    return client


@pytest.fixture
def authenticated_staff_client(privileged_staff_user):
    client = Client()
    client.login(username=privileged_staff_user.email, password=TEST_PASSWORD)
    return client


@pytest.fixture
def authenticated_superuser_client(superuser):
    client = Client()
    client.login(username=superuser.email, password=TEST_PASSWORD)
    return client
