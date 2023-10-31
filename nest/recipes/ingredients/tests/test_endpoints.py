import pytest
from django.urls import reverse

from nest.products.tests.utils import create_product

from ..endpoints import (
    recipe_ingredient_create_api,
    recipe_ingredient_delete_api,
    recipe_ingredient_groups_create_api,
    recipe_ingredient_groups_list_api,
    recipe_ingredient_list_api,
)

pytestmark = pytest.mark.django_db


class TestEndpointRecipeIngredientCreateAPI:
    ENDPOINT = reverse("api-1.0.0:recipe_ingredient_create_api")

    def test_anonymous_request_ingredient_create_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated non-staff users gets a 401 unauthorized when trying to
        create ingredients.
        """

        client = authenticated_client
        service_mock = mocker.patch(
            f"{recipe_ingredient_create_api.__module__}.create_recipe_ingredient"
        )
        product = create_product()
        payload = {"title": "Ingredient 1", "product": product.id}

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT, data=payload, content_type="application/json"
            )

        assert response.status_code == 401
        assert service_mock.call_count == 0

    def test_staff_request_ingredient_create_api(
        self, django_assert_num_queries, authenticated_staff_client, mocker
    ):
        """
        Test that staff users are able to create ingredients.
        """
        client = authenticated_staff_client
        service_mock = mocker.patch(
            f"{recipe_ingredient_create_api.__module__}.create_recipe_ingredient"
        )
        product = create_product()
        payload = {"title": "Ingredient 1", "product": product.id}

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT, data=payload, content_type="application/json"
            )

        assert response.status_code == 201
        assert service_mock.call_count == 1


class TestEndpointRecipeIngredientListAPI:
    ENDPOINT = reverse("api-1.0.0:recipe_ingredient_list_api")

    def test_anonymous_request_ingredient_list_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated non-staff users are able to retrieve a list of
        ingredients.
        """

        client = authenticated_client
        selector_mock = mocker.patch(
            f"{recipe_ingredient_list_api.__module__}.get_recipe_ingredients",
            return_value=[],
        )

        with django_assert_num_queries(2):
            response = client.get(self.ENDPOINT, content_type="application/json")

        assert response.status_code == 200
        assert selector_mock.call_count == 1


class TestEndpointRecipeIngredientDeleteAPI:
    ENDPOINT = reverse("api-1.0.0:recipe_ingredient_delete_api")

    def test_anonymous_request_ingredient_delete_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated non-staff users gets a 401 unauthorized when trying to
        delete ingredients.
        """

        client = authenticated_client
        service_mock = mocker.patch(
            f"{recipe_ingredient_delete_api.__module__}.delete_recipe_ingredient"
        )

        payload = {"ingredient_id": 1}
        with django_assert_num_queries(2):
            response = client.delete(
                self.ENDPOINT, data=payload, content_type="application/json"
            )

        assert response.status_code == 401
        assert service_mock.call_count == 0

    def test_staff_request_ingredient_create_api(
        self, django_assert_num_queries, authenticated_staff_client, mocker
    ):
        """
        Test that staff users are able to delete ingredients.
        """
        client = authenticated_staff_client
        service_mock = mocker.patch(
            f"{recipe_ingredient_delete_api.__module__}.delete_recipe_ingredient"
        )

        payload = {"ingredient_id": 1}
        with django_assert_num_queries(2):
            response = client.delete(
                self.ENDPOINT, data=payload, content_type="application/json"
            )

        assert response.status_code == 200
        assert service_mock.call_count == 1


class TestEndpointRecipeIngredientGroupsCreate:
    ENDPOINT = reverse("api-1.0.0:recipe_ingredient_groups_create_api", args=[1])

    def test_anonymous_request_recipe_ingredient_groups_create_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated non-staff users gets a 401 unauthorized when trying to
        create recipe ingredient item groups.
        """

        client = authenticated_client
        service_mock = mocker.patch(
            f"{recipe_ingredient_groups_create_api.__module__}"
            f".create_recipe_ingredient_item_groups"
        )

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT,
                data=[],
                content_type="application/json",
            )

        assert response.status_code == 401
        assert service_mock.call_count == 0

    def test_staff_request_recipe_ingredient_groups_create_api(
        self, django_assert_num_queries, authenticated_staff_client, mocker
    ):
        """
        Test that staff users are able to create ingredient item groups related to a
        recipe.
        """

        client = authenticated_staff_client
        service_mock = mocker.patch(
            f"{recipe_ingredient_groups_create_api.__module__}"
            f".create_recipe_ingredient_item_groups"
        )

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT,
                data=[],
                content_type="application/json",
            )

        assert response.status_code == 201
        assert service_mock.call_count == 1


class TestEndpointRecipeIngredientGroupsList:
    ENDPOINT = reverse("api-1.0.0:recipe_ingredient_groups_list_api", args=[1])

    def test_anonymous_request_recipe_ingredient_groups_list_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated non-staff users successfully can list ingredient item
        groups related to a recipe.
        """

        client = authenticated_client
        selector_mock = mocker.patch(
            f"{recipe_ingredient_groups_list_api.__module__}"
            f".get_recipe_ingredient_item_groups_for_recipe",
            return_value=[],
        )

        with django_assert_num_queries(2):
            response = client.get(
                self.ENDPOINT,
                content_type="application/json",
            )

        assert response.status_code == 200
        assert selector_mock.call_count == 1
