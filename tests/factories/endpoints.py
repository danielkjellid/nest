from collections import namedtuple
from dataclasses import dataclass, field
from typing import Any, Callable, Literal
from unittest.mock import MagicMock
from inspect import isclass
import structlog
from django.test.client import Client

logger = structlog.get_logger()

HTTP_METHOD = Literal["GET", "POST", "PUT", "DELETE"]

FactoryMock = namedtuple("FactoryMock", ["caller", "return_value"])
FactoryObjMock = namedtuple("FactoryObjMock", ["obj", "caller", "return_value"])


@dataclass
class Endpoint:
    url: str
    view_func: Callable
    mocks: list[FactoryMock | FactoryObjMock] | None = field(default_factory=[])
    method: HTTP_METHOD = "GET"
    payload: dict[str, Any] | None = None
    content_type: str = "application/json"


@dataclass
class Request:
    client: Callable[[..., Any], Client]
    expected_status_code: int
    expected_mock_calls: dict[str, int]
    help: str


class EndpointFactory:
    def __init__(self, endpoint: Endpoint, requests: dict[str, Request]):
        self.endpoint = endpoint
        self.requests = requests

    def _make_request_and_assert(
        self,
        request: Request,
        method: HTTP_METHOD,
        url: str,
        payload: dict[str, Any],
        content_type: str,
        caller_mocks: dict[str, MagicMock],
    ):
        """
        Make a single request for a member of the "self.requests" dict.
        """
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

        # Each request defines a dict of mocks and expected call count, assert those
        # values here.
        for mock_name, call_count in request.expected_mock_calls.items():
            mock = caller_mocks[mock_name]
            assert mock.call_count == call_count

            # Since requests are ran iteratively, this has to be reset after assert, or
            # else, you get an n+1.
            mock.reset_mock()

    def make_requests_and_assert(self, mocker: MagicMock):
        """
        Iterate through "self.requests" making a http request for each of them, asserting
        the status code and endpoint mock call count.
        """

        if self.endpoint.method == "GET" and self.endpoint.payload is not None:
            raise RuntimeError(
                "Sending payload with GET method, forgot to set the method on the "
                "Endpoint dataclass?"
            )

        caller_mocks = {}

        # Iterate over defined endpoint mocks and add them to a dict with the mock
        # name as key, and the mock itself as value.
        for factory_mocker in self.endpoint.mocks:
            print(factory_mocker)
            if isclass(factory_mocker[0]):
                print(factory_mocker)
                mock = factory_mocker[1]
                caller_mock = mocker.patch.object(
                    factory_mocker[0], mock, return_value=factory_mocker[2]
                )
            else:
                mock = factory_mocker[0]
                caller_mock = mocker.patch(
                    f"{self.endpoint.view_func.__module__}.{mock}",
                    return_value=factory_mocker[1],
                )

            caller_mocks[mock] = caller_mock

        # Make each request defined respectively.
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
