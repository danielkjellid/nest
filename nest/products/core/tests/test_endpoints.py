import pytest
from django.urls import reverse
from ..endpoints import (
    product_create_api,
    product_edit_api,
    product_list_api,
    product_detail_api,
)
from ..records import ProductRecord, ProductClassifiersRecord
from nest.units.tests.utils import get_unit
from django.test.client import MULTIPART_CONTENT
from ..models import Product
from decimal import Decimal
from nest.units.records import UnitRecord

pytestmark = pytest.mark.django_db


class TestEndpointProductCreateAPI:
    ENDPOINT = reverse("api-1.0.0:product_create_api")

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


class TestEndpointProductEditAPI:
    ENDPOINT = reverse("api-1.0.0:product_edit_api", args=[1])

    def test_anonymous_request_product_edit_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated users gets a 401 unauthorized when trying to edit
        products.
        """

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
                self.ENDPOINT,
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
                self.ENDPOINT,
                data=payload,
                content_type=MULTIPART_CONTENT,
            )

        assert response.status_code == 200
        assert service_mock.call_count == 1


class TestEndpointProductListAPI:
    ENDPOINT = reverse("api-1.0.0:product_list_api")

    def test_anonymous_request_product_list_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated users is able to retrieve a list of products.
        """

        client = authenticated_client
        selector_mock = mocker.patch(
            f"{product_list_api.__module__}.get_products", return_value=[]
        )

        with django_assert_num_queries(2):
            response = client.get(
                self.ENDPOINT,
                content_type="application/json",
            )

        assert response.status_code == 200
        assert selector_mock.call_count == 1


class TestEndpointProductDetailAPI:
    ENDPOINT = reverse("api-1.0.0:product_detail_api", args=[1])

    def test_anonymous_request_product_detail_api(
        self, django_assert_num_queries, authenticated_client, mocker
    ):
        """
        Test that authenticated users is able to retrieve a single product instance.
        """

        client = authenticated_client
        product_selector_mock = mocker.patch(
            f"{product_detail_api.__module__}.get_product",
            return_value=ProductRecord(
                id=1,
                name="Product",
                full_name="Some product",
                gross_price=Decimal("100.00"),
                gross_unit_price=None,
                unit=UnitRecord.from_unit(get_unit(abbreviation="g")),
                unit_quantity=Decimal("1.00"),
                oda_id=None,
                oda_url=None,
                is_available=True,
                is_synced=True,
                last_synced_at=None,
                thumbnail_url=None,
                gtin=None,
                supplier=None,
                display_price="100.00",
                is_oda_product=False,
                last_data_update=None,
                ingredients=None,
                allergens=None,
                classifiers=ProductClassifiersRecord(
                    contains_gluten=False, contains_lactose=False
                ),
                energy_kj=None,
                energy_kcal=None,
                fat=None,
                fat_saturated=None,
                fat_monounsaturated=None,
                fat_polyunsaturated=None,
                carbohydrates=None,
                carbohydrates_sugars=None,
                carbohydrates_starch=None,
                carbohydrates_polyols=None,
                fibres=None,
                protein=None,
                salt=None,
                sodium=None,
            ),
        )
        log_selector_mock = mocker.patch(
            f"{product_detail_api.__module__}.get_log_entries_for_object",
            return_value=[],
        )
        nutrition_selector_mock = mocker.patch(
            f"{product_detail_api.__module__}.get_nutrition_table", return_value=[]
        )

        with django_assert_num_queries(2):
            response = client.get(
                self.ENDPOINT,
                content_type="application/json",
            )

        assert response.status_code == 200
        assert product_selector_mock.call_count == 1
        assert nutrition_selector_mock.call_count == 1
        log_selector_mock.assert_called_once_with(model=Product, pk=1)
