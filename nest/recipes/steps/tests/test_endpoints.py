import pytest
from django.urls import reverse
from store_kit.http import status

from ..endpoints import (
    recipe_steps_create_api,
)

pytestmark = pytest.mark.django_db


class TestEndpointRecipeStepsCreateAPI:
    ENDPOINT = reverse("api-1.0.0:recipe_steps_create_api", args=[1])

    def test_anonymous_request_recipe_steps_create_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated non-staff users gets a 401 unauthorized when trying to
        create recipe ingredient item groups.
        """

        client = authenticated_client
        service_mock = mocker.patch(
            f"{recipe_steps_create_api.__module__}" f".create_recipe_steps"
        )

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT,
                data=[],
                content_type="application/json",
            )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert service_mock.call_count == 0

    def test_staff_request_recipe_ingredient_groups_create_api(
        self, django_assert_num_queries, authenticated_staff_client, mocker
    ):
        """
        Test that staff users are able to create steps related to a recipe.
        """

        client = authenticated_staff_client
        service_mock = mocker.patch(
            f"{recipe_steps_create_api.__module__}" f".create_recipe_steps"
        )

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT,
                data=[],
                content_type="application/json",
            )

        assert response.status_code == status.HTTP_201_CREATED
        assert service_mock.call_count == 1
