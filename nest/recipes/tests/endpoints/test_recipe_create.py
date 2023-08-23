import pytest
from django.urls import reverse

from nest.recipes.endpoints.recipe_create import recipe_create_api
from nest.recipes.enums import RecipeDifficulty, RecipeStatus

pytestmark = pytest.mark.django_db


class TestEndpointRecipeCreate:
    ENDPOINT = reverse("api-1.0.0:recipe_create_api")

    def test_anonymous_request_recipe_create_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated non-staff users gets a 401 unauthorized when trying to
        create recipes.
        """

        client = authenticated_client
        service_mock = mocker.patch(f"{recipe_create_api.__module__}.create_recipe")

        payload = {
            "title": "A new recipe",
            "search_keywords": None,
            "default_num_portions": 3,
            "status": str(RecipeStatus.PUBLISHED.value),
            "difficulty": str(RecipeDifficulty.MEDIUM.value),
            "external_id": None,
            "external_url": None,
            "is_vegetarian": False,
            "is_pescatarian": False,
        }

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT, data=payload, content_type="application/json"
            )

        assert response.status_code == 401
        assert service_mock.call_count == 0

    def test_staff_request_recipe_create_api(
        self, django_assert_num_queries, authenticated_staff_client, mocker
    ):
        """
        Test that staff users are able to create recipes.
        """

        client = authenticated_staff_client
        service_mock = mocker.patch(f"{recipe_create_api.__module__}.create_recipe")

        payload = {
            "title": "A new recipe",
            "search_keywords": None,
            "default_num_portions": 3,
            "status": str(RecipeStatus.PUBLISHED.value),
            "difficulty": str(RecipeDifficulty.MEDIUM.value),
            "external_id": None,
            "external_url": None,
            "is_vegetarian": False,
            "is_pescatarian": False,
        }

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT, data=payload, content_type="application/json"
            )

        assert response.status_code == 201
        assert service_mock.call_count == 1
