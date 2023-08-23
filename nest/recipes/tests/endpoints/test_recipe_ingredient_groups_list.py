import pytest

from nest.recipes.endpoints.recipe_ingredient_groups_list import (
    recipe_ingredient_groups_list_api,
)

from ..utils import create_recipe

pytestmark = pytest.mark.django_db


class TestEndpointRecipeIngredientGroupsList:
    BASE_ENDPOINT = "/api/v1/recipes"

    def test_anonymous_request_recipe_ingredient_groups_list_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated non-staff users successfully can list ingredient item
        groups related to a recipe.
        """

        recipe = create_recipe()

        client = authenticated_client
        selector_mock = mocker.patch(
            f"{recipe_ingredient_groups_list_api.__module__}"
            f".get_ingredient_item_groups_for_recipe",
            return_value=[],
        )

        with django_assert_num_queries(2):
            response = client.get(
                f"{self.BASE_ENDPOINT}/{recipe.id}/ingredient-groups/",
                content_type="application/json",
            )

        assert response.status_code == 200
        assert selector_mock.call_count == 1
