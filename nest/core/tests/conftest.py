import pytest
import requests_mock
from unittest import mock
import django.db.transaction

from nest.core.clients import BaseHTTPClient


################
# HTTP Clients #
################


@pytest.fixture
def request_mock():
    with requests_mock.mock() as m:
        yield m


@pytest.fixture
def http_client(requests_mock):
    class HTTPClient(BaseHTTPClient):
        enabled = True
        base_url = "http://127.0.0.1"
        auth_token = "token"

    return HTTPClient


###########
# Storage #
###########


@pytest.fixture(autouse=True)
def create_temp_storage(settings, tmp_path):
    settings.DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    settings.MEDIA_ROOT = tmp_path
    yield


@pytest.fixture
def immediate_on_commit():
    """
    Returns a context manager that's useful when writing test that waits on
    the transaction.on_commit(...) callback.
    """

    return mock.patch.object(django.db.transaction, "on_commit", lambda t: t())
