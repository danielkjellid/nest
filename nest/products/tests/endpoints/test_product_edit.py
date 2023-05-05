import pytest
from nest.products.endpoints.product_edit import product_edit_api
from django.test.client import MULTIPART_CONTENT
from nest.products.tests.utils import create_product
from nest.units.tests.utils import get_unit

pytestmark = pytest.mark.django_db


class TestEndpointProductEdit:
    ENDPOINT = "/api/v1/products"

    def test_anonymous_request_product_edit_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated users gets a 401 unauthorized when trying to edit
        products.
        """

        product = create_product()
        client = authenticated_client
        service_mock = mocker.patch(f"{product_edit_api.__module__}.edit_product")

        payload = {
            "name": "Some cool product",
            "gross_price": "100.00",
            "unit_quantity": "1",
            "unit": get_unit().id,
            "supplier": "Cool supplier",
            "is_available": True,
            "is_synced": True,
        }

        with django_assert_num_queries(2):
            response = client.post(
                f"{self.ENDPOINT}/{product.id}/edit/",
                data=payload,
                content_type=MULTIPART_CONTENT,
            )

        assert response.status_code == 401
        assert service_mock.call_count == 0

    def test_staff_request_product_edit_api(
        self, django_assert_num_queries, authenticated_staff_client, mocker
    ):
        """
        Test that staff users get a successful response when trying to edit products.
        """

        product = create_product()
        client = authenticated_staff_client
        service_mock = mocker.patch(f"{product_edit_api.__module__}.edit_product")

        payload = {
            "name": "Some cool product",
            "gross_price": "100.00",
            "unit_quantity": "1",
            "unit": get_unit().id,
            "supplier": "Cool supplier",
            "is_available": True,
            "is_synced": True,
        }

        with django_assert_num_queries(2):
            response = client.post(
                f"{self.ENDPOINT}/{product.id}/edit/",
                data=payload,
                content_type=MULTIPART_CONTENT,
            )

        assert response.status_code == 200
        assert service_mock.call_count == 1
