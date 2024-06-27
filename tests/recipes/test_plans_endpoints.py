from unittest.mock import MagicMock

import pytest
from django.urls import reverse
from store_kit.http import status

from nest.recipes.plans.endpoints import recipe_plan_list_for_home_api
from tests.factories.endpoints import Endpoint, EndpointFactory, FactoryMock, Request
from tests.factories.records import ReipcePlanRecordFactory
from tests.helpers.clients import authenticated_client

recipe_plan_list_for_home_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:recipe_plan_list_for_home_api", args=[1]),
        view_func=recipe_plan_list_for_home_api,
        mocks=[
            FactoryMock("get_recipe_plans_for_home", [ReipcePlanRecordFactory.build()])
        ],
    ),
    requests={
        "authenticated_request": Request(
            help="Test that normal users are able to get a list of recipe_plans",
            client=authenticated_client,
            expected_status_code=status.HTTP_200_OK,
            expected_mock_calls={"get_recipe_plans_for_home": 1},
        ),
    },
)

request_factories = [recipe_plan_list_for_home_api_factory]


@pytest.mark.parametrize("factory", request_factories)
@pytest.mark.django_db
def test_recipes_core_endpoints(factory: EndpointFactory, mocker: MagicMock) -> None:
    factory.make_requests_and_assert(mocker)
