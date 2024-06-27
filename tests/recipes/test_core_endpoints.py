from unittest.mock import MagicMock

import pytest
from django.urls import reverse
from store_kit.http import status

from nest.recipes.core.endpoints import (
    recipe_create_api,
    recipe_detail_api,
    recipe_list_api,
)
from nest.recipes.core.enums import RecipeDifficulty, RecipeStatus

from ..factories.endpoints import Endpoint, EndpointFactory, FactoryMock, Request
from ..factories.records import RecipeDetailRecordFactory, RecipeRecordFactory
from ..helpers.clients import (
    anonymous_client,
    authenticated_client,
    authenticated_staff_client,
)

recipe_create_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:recipe_create_api"),
        method="POST",
        view_func=recipe_create_api,
        mocks=[FactoryMock("create_recipe", None)],
        payload={
            "base_recipe": {
                "title": "A new recipe",
                "search_keywords": None,
                "default_num_portions": 3,
                "status": str(RecipeStatus.PUBLISHED.value),
                "difficulty": str(RecipeDifficulty.MEDIUM.value),
                "external_id": None,
                "external_url": None,
                "is_vegetarian": False,
                "is_pescatarian": False,
            },
            "steps": [
                {
                    "number": 1,
                    "duration": 5,
                    "instruction": "Some instruction for step 1",
                    "step_type": "cooking",
                    "ingredient_items": [
                        {
                            "ingredient": "1",
                            "portion_quantity": "150",
                            "portion_quantity_unit": "1",
                            "additional_info": None,
                        },
                        {
                            "ingredient": "2",
                            "portion_quantity": "200",
                            "portion_quantity_unit": "1",
                            "additional_info": None,
                        },
                        {
                            "ingredient": "3",
                            "portion_quantity": "190",
                            "portion_quantity_unit": "1",
                            "additional_info": None,
                        },
                    ],
                },
            ],
            "ingredient_item_groups": [
                {
                    "title": "Cod with peppers",
                    "ordering": 1,
                    "ingredient_items": [
                        {
                            "ingredient": "1",
                            "additional_info": None,
                            "portion_quantity": "100",
                            "portion_quantity_unit": "1",
                        },
                        {
                            "ingredient": "2",
                            "additional_info": "Descaled",
                            "portion_quantity": "1",
                            "portion_quantity_unit": "1",
                        },
                    ],
                },
                {
                    "title": "Accessories",
                    "ordering": 2,
                    "ingredient_items": [
                        {
                            "ingredient": "2",
                            "additional_info": None,
                            "portion_quantity": "20",
                            "portion_quantity_unit": "1",
                        }
                    ],
                },
            ],
        },
    ),
    requests={
        "authenticated_request": Request(
            help="Test that normal users are unable to create recipes.",
            client=authenticated_client,
            expected_status_code=status.HTTP_401_UNAUTHORIZED,
            expected_mock_calls={"create_recipe": 0},
        ),
        "staff_request": Request(
            help="Test that staff users are able to create new recipes.",
            client=authenticated_staff_client,
            expected_status_code=status.HTTP_201_CREATED,
            expected_mock_calls={"create_recipe": 1},
        ),
    },
)

recipe_list_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:recipe_list_api"),
        view_func=recipe_list_api,
        mocks=[FactoryMock("get_recipes", [RecipeDetailRecordFactory.build()])],
    ),
    requests={
        "authenticated_request": Request(
            help="Test that normal users are able to get a list of recipes",
            client=authenticated_client,
            expected_status_code=status.HTTP_200_OK,
            expected_mock_calls={"get_recipes": 1},
        ),
    },
)

recipe_detail_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:recipe_detail_api", args=[1]),
        view_func=recipe_detail_api,
        mocks=[FactoryMock("get_recipe", RecipeDetailRecordFactory.build())],
    ),
    requests={
        "anonymous_request": Request(
            help="Test that anonymous users are able to retrieve recipe details.",
            client=anonymous_client,
            expected_status_code=status.HTTP_200_OK,
            expected_mock_calls={"get_recipe": 1},
        ),
    },
)

request_factories = [
    recipe_create_api_factory,
    recipe_list_api_factory,
    recipe_detail_api_factory,
]


@pytest.mark.parametrize("factory", request_factories)
@pytest.mark.django_db
def test_recipes_core_endpoints(factory: EndpointFactory, mocker: MagicMock) -> None:
    factory.make_requests_and_assert(mocker)
