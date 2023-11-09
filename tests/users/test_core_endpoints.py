from unittest.mock import MagicMock

import pytest
from django.urls import reverse
from store_kit.http import status

from nest.users.core.endpoints import user_list_api

from ..factories.endpoints import Endpoint, EndpointFactory, FactoryMock, Request
from ..helpers.clients import authenticated_client, authenticated_staff_client

user_list_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:user_list_api"),
        view_func=user_list_api,
        mocks=[FactoryMock("get_users", [])],
    ),
    requests={
        "authenticated_request": Request(
            client=authenticated_client,
            expected_status_code=status.HTTP_401_UNAUTHORIZED,
            expected_mock_calls={"get_users": 0},
        ),
        "staff_request": Request(
            client=authenticated_staff_client,
            expected_status_code=status.HTTP_200_OK,
            expected_mock_calls={"get_users": 1},
        ),
    },
)

request_factories = [user_list_api_factory]


@pytest.mark.parametrize("factory", request_factories)
@pytest.mark.django_db
def test_users_core_endpoints(factory: EndpointFactory, mocker: MagicMock) -> None:
    factory.make_requests_and_assert(mocker)
