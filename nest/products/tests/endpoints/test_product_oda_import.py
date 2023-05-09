import pytest
from nest.data_pools.providers.oda.clients import OdaClient
from nest.data_pools.tests.oda.utils import get_oda_product_response_dict
from nest.data_pools.providers.oda.records import OdaProductDetailRecord

pytestmark = pytest.mark.django_db


class TestEndpointProductOdaImport:
    ENDPOINT = "/api/v1/products/oda/import/"

    def test_client_request_product_oda_import_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that anonymous users gets a 401 unauthorized when trying to import Oda
        products.
        """

        client = authenticated_client
        service_mock = mocker.patch.object(OdaClient, "get_product")

        payload = {"odaProductId": 459}

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT, data=payload, content_type="application/json"
            )

        assert response.status_code == 401
        assert service_mock.call_count == 0

    def test_staff_request_product_oda_import_api(
        self, django_assert_num_queries, authenticated_staff_client, mocker
    ):
        """
        Test that staff users get a successful response when trying to import an Oda
        product.
        """

        client = authenticated_staff_client
        service_mock = mocker.patch.object(
            OdaClient,
            "get_product",
            return_value=OdaProductDetailRecord(
                **get_oda_product_response_dict(id=459)
            ),
        )

        payload = {"odaProductId": 459}

        with django_assert_num_queries(2):
            response = client.post(
                self.ENDPOINT, data=payload, content_type="application/json"
            )

        assert response.status_code == 200
        assert service_mock.call_count == 1
