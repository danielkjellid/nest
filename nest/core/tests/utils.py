from nest.users.models import User
from django.test.client import RequestFactory
from django.core.handlers.wsgi import WSGIRequest


def create_request(*, user: User | None = None, addr: str = "127.0.0.1") -> WSGIRequest:
    request_factory = RequestFactory()
    request = request_factory.get(
        "/users/",
        {"param": "foo"},
        **{"HTTP_USER_AGENT": "firefox-22", "REMOTE_ADDR": addr},
    )
    request.session = {}

    if user is not None:
        request.user = user

    return request
