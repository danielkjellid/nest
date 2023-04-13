import pytest
from django.test import Client
from nest.users.tests.conftest import *  # noqa


@pytest.fixture
def anonymous_client_fixture():
    return Client()


@pytest.fixture
def authenticated_client(user_fixture):
    client = Client()
    client.login(username=user_fixture.email, password=TEST_PASSWORD)
    return client


@pytest.fixture
def authenticated_staff_client(staff_user_fixture):
    client = Client()
    client.login(username=staff_user_fixture.email, password=TEST_PASSWORD)
    return client


@pytest.fixture
def authenticated_superuser_client(superuser_fixture):
    client = Client()
    client.login(username=superuser_fixture.email, password=TEST_PASSWORD)
    return client
