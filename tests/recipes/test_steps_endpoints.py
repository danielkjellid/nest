from unittest.mock import MagicMock

import pytest
from django.urls import reverse
from store_kit.http import status

from nest.recipes.steps.endpoints import recipe_steps_create_api
from nest.recipes.steps.enums import RecipeStepType

from ..factories.endpoints import (
    Endpoint,
    EndpointFactory,
    FactoryMock,
    Request,
)
from ..helpers.clients import authenticated_client, authenticated_staff_client

recipe_steps_create_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:recipe_steps_create_api", args=[1]),
        method="POST",
        view_func=recipe_steps_create_api,
        mocks=[FactoryMock("create_recipe_steps", None)],
        payload=[
            {
                "number": 1,
                "duration": 10,
                "instruction": "Instruction",
                "step_type": str(RecipeStepType.COOKING),
                "ingredient_items": ["1", "2"],
            }
        ],
    ),
    requests={
        "authenticated_request": Request(
            help="Test that normal users are unable to create recipe steps",
            client=authenticated_client,
            expected_status_code=status.HTTP_401_UNAUTHORIZED,
            expected_mock_calls={"create_recipe_steps": 0},
        ),
        "staff_request": Request(
            help="Test that staff users are able to create recipe steps",
            client=authenticated_staff_client,
            expected_status_code=status.HTTP_201_CREATED,
            expected_mock_calls={"create_recipe_steps": 1},
        ),
    },
)

request_factories = [recipe_steps_create_api_factory]


@pytest.mark.parametrize("factory", request_factories)
@pytest.mark.django_db
def test_recipes_steps_endpoints(factory: EndpointFactory, mocker: MagicMock) -> None:
    factory.make_requests_and_assert(mocker)
