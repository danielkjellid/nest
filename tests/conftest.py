import pytest
import requests_mock
from unittest import mock
import django.db.transaction
from .products.fixtures import *  # noqa
from .units.fixtures import *  # noqa
from .recipes.fixtures import *  # noqa
from nest.core.clients import BaseHTTPClient
from collections.abc import Mapping


################
# Spec helpers #
################


@pytest.fixture
def spec():
    def _spec(request_spec, default_spec):
        default_spec = default_spec.copy()

        if not request_spec or not isinstance(request_spec, dict):
            return default_spec

        def update_spec(
            original: dict[str, Any], new: dict[str, Any]
        ) -> dict[str, Any]:
            for key, value in new.items():
                if isinstance(value, Mapping):
                    original[key] = update_spec(original.get(key, {}), value)
                else:
                    original[key] = value
            return original

        return update_spec(default_spec, request_spec)

    return _spec


@pytest.fixture
def create_instances(request: pytest.FixtureRequest, spec):
    def _create_instances(create_callback, default_spec, marker_name):
        instances = {}

        for marker in request.node.iter_markers(marker_name):
            assert not marker.args, "Only kwargs is accepted with this fixture"

            for slug in marker.kwargs:
                request_spec = marker.kwargs.get(slug, {})
                instances[slug] = create_callback(spec(request_spec, default_spec))

        return instances

    return _create_instances


@pytest.fixture
def create_instance(request: pytest.FixtureRequest, spec):
    def _create_instance(create_callback, default_spec, marker_name):
        marker = request.node.get_closest_marker(marker_name)
        assert not getattr(
            marker, "args", None
        ), "Only kwargs is accepted with this fixture"
        request_spec = getattr(marker, "kwargs", None) or default_spec

        return create_callback(spec(request_spec, default_spec))

    return _create_instance


@pytest.fixture
def get_related_instance():
    def _get_related_instance(
        key: str, spec: dict[str, Any], related_instance, related_instances
    ):
        value_from_spec = spec.pop(key, None)

        if value_from_spec == "default":
            return related_instance
        return related_instances.get(value_from_spec)

    return _get_related_instance


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
