import pytest
from django.urls import reverse

from nest.ingredients.endpoints.ingredient_create import ingredient_create_api
from nest.products.tests.utils import create_product

pytestmark = pytest.mark.django_db


class TestEndpointIngredientCreate:
    ENDPOINT = reverse("api-1.0.0:ingredient_create_api")

    def test_anonymous_request_ingredient_create_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated non-staff users gets a 401 unauthorized when trying to
        create ingredients.
        """

        client = authenticated_client
        service_mock = mocker.patch(
            f"{ingredient_create_api.__module__}.create_ingredient"
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
            f"{ingredient_create_api.__module__}.create_ingredient"
        )
        product = create_product()
        payload = {"title": "Ingredient 1", "product": product.id}

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT, data=payload, content_type="application/json"
            )

        assert response.status_code == 201
        assert service_mock.call_count == 1
