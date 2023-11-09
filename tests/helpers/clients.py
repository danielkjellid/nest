from django.test import Client

from .users import TEST_USER_PASSWORD, staff_user, superuser, user


def anonymous_client():
    return Client()


def authenticated_client():
    client = Client()
    client.login(username=user().email, password=TEST_USER_PASSWORD)
    return client


def authenticated_staff_client():
    client = Client()
    client.login(username=staff_user().email, password=TEST_USER_PASSWORD)
    return client


def authenticated_superuser_client():
    client = Client()
    client.login(username=superuser().email, password=TEST_USER_PASSWORD)
    return client
