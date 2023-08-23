import pytest

from nest.recipes.endpoints.recipe_steps_create import (
    recipe_steps_create_api,
)

from ..utils import create_recipe

pytestmark = pytest.mark.django_db


class TestEndpointRecipeStepsCreate:
    BASE_ENDPOINT = "/api/v1/recipes"

    def test_anonymous_request_recipe_ingredient_groups_create_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated non-staff users gets a 401 unauthorized when trying to
        create recipe ingredient item groups.
        """

        recipe = create_recipe()

        client = authenticated_client
        service_mock = mocker.patch(
            f"{recipe_steps_create_api.__module__}" f".create_recipe_steps"
        )

        with django_assert_num_queries(2):
            response = client.post(
                f"{self.BASE_ENDPOINT}/{recipe.id}/steps/create/",
                data=[],
                content_type="application/json",
            )

        assert response.status_code == 401
        assert service_mock.call_count == 0

    def test_staff_request_recipe_ingredient_groups_create_api(
        self, django_assert_num_queries, authenticated_staff_client, mocker
    ):
        """
        Test that staff users are able to create steps related to a recipe.
        """

        recipe = create_recipe()

        client = authenticated_staff_client
        service_mock = mocker.patch(
            f"{recipe_steps_create_api.__module__}" f".create_recipe_steps"
        )

        with django_assert_num_queries(2):
            response = client.post(
                f"{self.BASE_ENDPOINT}/{recipe.id}/steps/create/",
                data=[],
                content_type="application/json",
            )

        assert response.status_code == 201
        assert service_mock.call_count == 1
