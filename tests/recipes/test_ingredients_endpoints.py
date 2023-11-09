from unittest.mock import MagicMock

import pytest
from django.urls import reverse
from store_kit.http import status

from nest.recipes.ingredients.endpoints import (
    recipe_ingredient_create_api,
    recipe_ingredient_delete_api,
    recipe_ingredient_groups_create_api,
    recipe_ingredient_groups_list_api,
    recipe_ingredient_list_api,
)

from ..factories.endpoints import Endpoint, EndpointFactory, FactoryMock, Request
from ..factories.records import (
    RecipeIngredientItemGroupRecordFactory,
    RecipeIngredientRecordFactory,
)
from ..helpers.clients import authenticated_client, authenticated_staff_client

recipe_ingredient_create_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:recipe_ingredient_create_api"),
        method="POST",
        view_func=recipe_ingredient_create_api,
        mocks=[FactoryMock("create_recipe_ingredient", None)],
        payload={"title": "Ingredient 1", "product": 1},
    ),
    requests={
        "authenticated_request": Request(
            help="Test that normal users are unable to create recipe ingredients",
            client=authenticated_client,
            expected_status_code=status.HTTP_401_UNAUTHORIZED,
            expected_mock_calls={"create_recipe_ingredient": 0},
        ),
        "staff_request": Request(
            help="Test that staff users are able to create recipe ingredients",
            client=authenticated_staff_client,
            expected_status_code=status.HTTP_201_CREATED,
            expected_mock_calls={"create_recipe_ingredient": 1},
        ),
    },
)

recipe_ingredient_list_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:recipe_ingredient_list_api"),
        view_func=recipe_ingredient_list_api,
        mocks=[
            FactoryMock(
                "get_recipe_ingredients", [RecipeIngredientRecordFactory.build()]
            )
        ],
    ),
    requests={
        "authenticated_request": Request(
            help="Test that normal users are able to retrieve a list of ingredients",
            client=authenticated_staff_client,
            expected_status_code=status.HTTP_200_OK,
            expected_mock_calls={"get_recipe_ingredients": 1},
        ),
    },
)

recipe_ingredient_delete_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:recipe_ingredient_delete_api"),
        method="DELETE",
        view_func=recipe_ingredient_delete_api,
        mocks=[FactoryMock("delete_recipe_ingredient", None)],
        payload={"ingredient_id": 1},
    ),
    requests={
        "authenticated_request": Request(
            help="Test that normal users are unable to delete recipe ingredients",
            client=authenticated_client,
            expected_status_code=status.HTTP_401_UNAUTHORIZED,
            expected_mock_calls={"delete_recipe_ingredient": 0},
        ),
        "staff_request": Request(
            help="Test that staff users are able to delete recipe ingredients",
            client=authenticated_staff_client,
            expected_status_code=status.HTTP_200_OK,
            expected_mock_calls={"delete_recipe_ingredient": 1},
        ),
    },
)

recipe_ingredient_groups_create_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:recipe_ingredient_groups_create_api", args=[1]),
        method="POST",
        view_func=recipe_ingredient_groups_create_api,
        mocks=[FactoryMock("create_recipe_ingredient_item_groups", None)],
        payload=[
            {
                "title": "Group 1",
                "ordering": 1,
                "ingredients": [
                    {
                        "ingredient": "1",
                        "portion_quantity": "1",
                        "unit": "1",
                        "additional_info": None,
                    }
                ],
            }
        ],
    ),
    requests={
        "authenticated_request": Request(
            help="Test that normal users are unable to create recipe ingredient item groups",
            client=authenticated_client,
            expected_status_code=status.HTTP_401_UNAUTHORIZED,
            expected_mock_calls={"create_recipe_ingredient_item_groups": 0},
        ),
        "staff_request": Request(
            help="Test that staff users are able to create recipe ingredient item groups",
            client=authenticated_staff_client,
            expected_status_code=status.HTTP_201_CREATED,
            expected_mock_calls={"create_recipe_ingredient_item_groups": 1},
        ),
    },
)

recipe_ingredient_groups_list_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:recipe_ingredient_groups_list_api", args=[1]),
        view_func=recipe_ingredient_groups_list_api,
        mocks=[
            FactoryMock(
                "get_recipe_ingredient_item_groups_for_recipe",
                [RecipeIngredientItemGroupRecordFactory.build()],
            )
        ],
    ),
    requests={
        "authenticated_request": Request(
            help=(
                "Test that normal users are unable to retrieve a list of recipe "
                "ingredient item groups"
            ),
            client=authenticated_client,
            expected_status_code=status.HTTP_401_UNAUTHORIZED,
            expected_mock_calls={"get_recipe_ingredient_item_groups_for_recipe": 0},
        ),
        "staff_request": Request(
            help=(
                "Test that staff users are able to retrieve a list of recipe "
                "ingredient item groups"
            ),
            client=authenticated_staff_client,
            expected_status_code=status.HTTP_200_OK,
            expected_mock_calls={"get_recipe_ingredient_item_groups_for_recipe": 1},
        ),
    },
)

request_factories = [
    recipe_ingredient_create_api_factory,
    recipe_ingredient_list_api_factory,
    recipe_ingredient_delete_api_factory,
    recipe_ingredient_groups_create_api_factory,
    recipe_ingredient_groups_list_api_factory,
]


@pytest.mark.parametrize("factory", request_factories)
@pytest.mark.django_db
def test_recipes_ingredients_endpoints(
    factory: EndpointFactory, mocker: MagicMock
) -> None:
    factory.make_requests_and_assert(mocker)
