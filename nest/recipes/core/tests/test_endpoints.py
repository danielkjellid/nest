from datetime import timedelta

import pytest
from django.urls import reverse

from store_kit.http import status

from ..endpoints import (
    recipe_create_api,
    recipe_detail_api,
    recipe_list_api,
)
from ..enums import RecipeDifficulty, RecipeStatus
from ..records import RecipeDetailRecord, RecipeDurationRecord

pytestmark = pytest.mark.django_db


class TestEndpointRecipeCreateAPI:
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

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
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

        assert response.status_code == status.HTTP_201_CREATED
        assert service_mock.call_count == 1


class TestEndpointRecipeListAPI:
    ENDPOINT = reverse("api-1.0.0:recipe_list_api")

    def test_anonymous_request_recipe_list_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated non-staff users successfully can list recipes.
        """

        client = authenticated_client
        selector_mock = mocker.patch(
            f"{recipe_list_api.__module__}.get_recipes", return_value=[]
        )

        with django_assert_num_queries(2):
            response = client.get(self.ENDPOINT, content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        assert selector_mock.call_count == 1


class TestEndpointRecipeDetailAPI:
    ENDPOINT = reverse("api-1.0.0:recipe_detail_api", args=[1])

    def test_anonymous_request_recipe_detail_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated non-staff users successfully can retrieve a recipe
        instance.
        """

        client = authenticated_client
        selector_mock = mocker.patch(
            f"{recipe_detail_api.__module__}.get_recipe",
            return_value=RecipeDetailRecord(
                id=1,
                title="Recipe title",
                slug="recipe-title",
                default_num_portions=4,
                search_keywords=None,
                external_id=None,
                external_url=None,
                status=RecipeStatus.PUBLISHED,
                status_display="published",
                difficulty=RecipeDifficulty.MEDIUM,
                difficulty_display="medium",
                is_vegetarian=False,
                is_pescatarian=False,
                duration=RecipeDurationRecord.from_datetime(
                    preparation_time=timedelta(seconds=120),
                    cooking_time=timedelta(seconds=120),
                    total_time=timedelta(seconds=240),
                ),
                glycemic_data=None,
                health_score=None,
                ingredient_groups=[],
                steps=[],
            ),
        )

        with django_assert_num_queries(2):
            response = client.get(self.ENDPOINT, content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        selector_mock.assert_called_once_with(pk=1)
