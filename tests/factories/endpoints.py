from collections import namedtuple
from dataclasses import dataclass, field
from typing import Any, Callable, Literal

import structlog
from django.test.client import Client

logger = structlog.get_logger()

FactoryMock = namedtuple("FactoryMock", ["caller", "return_value"])


@dataclass
class Endpoint:
    url: str
    view_func: Callable
    mocks: list[FactoryMock] | None = field(default_factory=[])
    method: Literal["GET", "POST", "PUT", "DELETE"] = "GET"
    payload: dict[str, Any] | None = None
    content_type: str = "application/json"


@dataclass
class Request:
    client: Callable[[..., Any], Client]
    expected_status_code: int
    expected_mock_calls: dict[str, int]


class EndpointFactory:
    def __init__(self, endpoint: Endpoint, requests: dict[str, Request]):
        self.endpoint = endpoint
        self.requests = requests

    def _make_request_and_assert(
        self, request: Request, method, url, payload, content_type, caller_mocks
    ):
        client = request.client()
        request_method = getattr(client, method.lower())

        response = request_method(
            url,
            data=payload,
            content_type=content_type,
        )
        logger.info(
            "Finished request",
            status_code=response.status_code,
            content=response.content,
        )

        assert response.status_code == request.expected_status_code
        for mock_name, call_count in request.expected_mock_calls.items():
            mock = caller_mocks[mock_name]
            assert mock.call_count == call_count

            # Since requests are ran iteratively, this has to be reset after assert.
            mock.reset_mock()

    def make_requests_and_assert(self, mocker):
        caller_mocks = {}

        for mock, return_value in self.endpoint.mocks:
            caller_mock = mocker.patch(
                f"{self.endpoint.view_func.__module__}.{mock}",
                return_value=return_value,
            )

            caller_mocks[mock] = caller_mock

        for key, request in self.requests.items():
            logger.info(
                "Making request", key=key, request=request, endpoint=self.endpoint
            )
            self._make_request_and_assert(
                request=request,
                method=self.endpoint.method,
                url=self.endpoint.url,
                payload=self.endpoint.payload,
                content_type=self.endpoint.content_type,
                caller_mocks=caller_mocks,
            )
