from django.test.client import Client
from typing import Literal, Callable, Any
from collections import namedtuple

FactoryMock = namedtuple("FactoryMock", ["caller", "return_value"])


class EndpointFactory:
    def __init__(
        self,
        *,
        url: str,
        endpoint: Callable,
        method: Literal["GET", "POST", "PUT", "DELETE"] = "GET",
        mocks: list[FactoryMock] = [],
        payload: dict[str, Any] | None = None,
        content_type: str = "application/json",
    ) -> None:
        self.url = url
        self.method = method
        self.endpoint = endpoint
        self.mocks = mocks
        self.payload = payload
        self.content_type = content_type


class EndpointRequest:
    def __init__(
        self, endpoint_factory: EndpointFactory, client: Callable[[..., Any], Client]
    ) -> None:
        self.endpoint_factory = endpoint_factory
        self.client = client

    def make_request_and_assert(
        self, mocker, status_code: int, call_counts: list[int]
    ) -> None:
        ef = self.endpoint_factory

        caller_mocks = []
        for mock, return_value in ef.mocks:
            caller_mock = mocker.patch(
                f"{ef.endpoint.__module__}.{mock}",
                return_value=return_value,
            )

            caller_mocks.append(caller_mock)

        client = self.client()
        request_method = getattr(client, ef.method.lower())

        response = request_method(
            ef.url,
            data=ef.payload,
            content_type=ef.content_type,
        )

        assert response.status_code == status_code
        for index, count in enumerate(call_counts):
            assert caller_mocks[index].call_count == count
