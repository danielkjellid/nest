import pytest

from nest.products.core.endpoints.product_oda_import_confirm import (
    product_oda_import_confirm_api,
)

pytestmark = pytest.mark.django_db


class TestEndpointProductOdaImportConfirm:
    ENDPOINT = "/api/v1/products/oda/import/confirm/"

    def test_client_request_product_oda_import_confirm_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that anonymous users gets a 401 unauthorized when trying to import Oda
        products.
        """

        client = authenticated_client
        service_mock = mocker.patch(
            f"{product_oda_import_confirm_api.__module__}.import_from_oda"
        )

        payload = {"odaProductId": 459}

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT, data=payload, content_type="application/json"
            )

        assert response.status_code == 401
        assert service_mock.call_count == 0

    def test_staff_request_product_oda_import_confirm_api(
        self, django_assert_num_queries, authenticated_staff_client, mocker
    ):
        """
        Test that staff users get a successful response when trying to import an Oda
        product.
        """

        client = authenticated_staff_client
        service_mock = mocker.patch(
            f"{product_oda_import_confirm_api.__module__}.import_from_oda"
        )

        payload = {"odaProductId": 459}

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT, data=payload, content_type="application/json"
            )

        assert response.status_code == 200
        assert service_mock.call_count == 1
