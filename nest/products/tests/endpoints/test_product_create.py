import pytest
from django.test.client import MULTIPART_CONTENT

from nest.products.endpoints.product_create import product_create_api
from nest.units.tests.utils import get_unit

pytestmark = pytest.mark.django_db


class TestEndpointProductCreate:
    ENDPOINT = "/api/v1/products/create/"

    def test_anonymous_request_product_create_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated users gets a 401 unauthorized when trying to create
        products.
        """

        client = authenticated_client
        service_mock = mocker.patch(f"{product_create_api.__module__}.create_product")

        payload = {
            "name": "Some cool product",
            "gross_price": "100.00",
            "unit_quantity": "1",
            "unit": get_unit().id,
            "supplier": "Cool supplier",
            "is_available": True,
        }

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT,
                data=payload,
                content_type=MULTIPART_CONTENT,
            )

        assert response.status_code == 401
        assert service_mock.call_count == 0

    def test_staff_request_product_create_api(
        self, django_assert_num_queries, authenticated_staff_client, mocker
    ):
        """
        Test that staff users are able to create products.
        """

        client = authenticated_staff_client
        service_mock = mocker.patch(f"{product_create_api.__module__}.create_product")

        payload = {
            "name": "Some cool product",
            "gross_price": "100.00",
            "unit_quantity": "1",
            "unit": get_unit().id,
            "supplier": "Cool supplier",
            "is_available": True,
        }

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT,
                data=payload,
                content_type=MULTIPART_CONTENT,
            )

        assert response.status_code == 200
        assert service_mock.call_count == 1
