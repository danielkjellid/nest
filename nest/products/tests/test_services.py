from decimal import Decimal

import pytest

from nest.data_pools.providers.oda.clients import OdaClient
from nest.products.models import Product
from nest.data_pools.providers.oda.records import OdaProductDetailRecord
from nest.products.services import ProductService
from nest.products.tests.utils import (
    create_product,
    get_unit,
    next_oda_id,
    create_product_image,
)
from nest.data_pools.tests.oda.utils import get_oda_product_response_dict

pytestmark = pytest.mark.django_db


class TestProductService:
    def test_update_or_create_product_with_pk(self, django_assert_num_queries):
        """
        Test that the update_or_create_product creates or updates as expected.
        """
        unit = get_unit(abbreviation="g")
        defaults = {
            "oda_id": next_oda_id(),
            "oda_url": "https://example.com/",
            "name": "New example product",
            "gross_price": Decimal("50.00"),
            "gross_unit_price": Decimal("50.00"),
            "unit_id": unit.id,
            "unit_quantity": Decimal("1.00"),
            "is_available": True,
            "supplier": "Test supplier",
        }

        assert Product.objects.all().count() == 0

        with django_assert_num_queries(7):
            ProductService.update_or_create_product(**defaults)

        assert Product.objects.all().count() == 1

        existing_product = create_product()
        assert existing_product.name == "Test product"

        defaults = {
            "oda_id": existing_product.oda_id,
            "oda_url": existing_product.oda_url,
            "name": "Updated test product",
            "gross_price": existing_product.gross_price,
            "gross_unit_price": existing_product.gross_unit_price,
            "unit_id": existing_product.unit_id,
            "unit_quantity": existing_product.unit_quantity,
            "is_available": existing_product.is_available,
            "supplier": existing_product.supplier,
        }

        with django_assert_num_queries(5):
            updated_product = ProductService.update_or_create_product(
                pk=existing_product.id, **defaults
            )

        assert updated_product.id == existing_product.id
        assert updated_product.name == "Updated test product"

    def test_update_or_create_product_with_oda_id(self, django_assert_num_queries):
        """ """
        existing_product = create_product()
        assert existing_product.name == "Test product"

        defaults = {
            "oda_url": existing_product.oda_url,
            "name": "Updated test product",
            "gross_price": existing_product.gross_price,
            "gross_unit_price": existing_product.gross_unit_price,
            "unit_id": existing_product.unit_id,
            "unit_quantity": existing_product.unit_quantity,
            "is_available": existing_product.is_available,
            "supplier": existing_product.supplier,
        }

        with django_assert_num_queries(5):
            updated_product = ProductService.update_or_create_product(
                oda_id=existing_product.oda_id, **defaults
            )

        assert updated_product.id == existing_product.id
        assert updated_product.name == "Updated test product"
        assert updated_product.oda_id == existing_product.oda_id

    def test_import_from_oda_excluded_from_sync(
        self, django_assert_num_queries, request_mock, mocker
    ):
        """
        Test that products marked as is_synced=False is returned early
        without any updates.
        """
        product = create_product(is_synced=False)
        product_response_request_mock = mocker.patch.object(
            OdaClient,
            "get_product",
            return_value=OdaProductDetailRecord(
                **get_oda_product_response_dict(id=product.oda_id)
            ),
        )
        product_image_response_request_mock = mocker.patch.object(
            OdaClient,
            "get_image",
            return_value=create_product_image(name="test"),
        )
        _validate_oda_response_mock = mocker.patch.object(
            ProductService, "_validate_oda_response"
        )

        with django_assert_num_queries(1):
            imported_product = ProductService.import_from_oda(
                oda_product_id=product.oda_id
            )

        assert imported_product is None

        assert product_response_request_mock.call_count == 1
        assert product_image_response_request_mock.call_count == 1
        assert _validate_oda_response_mock.call_count == 1

    def test_import_from_oda_new_product(
        self, django_assert_num_queries, request_mock, mocker
    ):
        """
        Test that the import_from_oda creates a new product if the product
        does not already exist.
        """

        assert Product.objects.all().count() == 0

        oda_id_mock = 3333

        product_response_request_mock = mocker.patch.object(
            OdaClient,
            "get_product",
            return_value=OdaProductDetailRecord(
                **get_oda_product_response_dict(id=oda_id_mock)
            ),
        )
        product_image_response_request_mock = mocker.patch.object(
            OdaClient,
            "get_image",
            return_value=create_product_image(name="test"),
        )
        _validate_oda_response_mock = mocker.patch.object(
            ProductService, "_validate_oda_response"
        )

        with django_assert_num_queries(11):
            imported_product = ProductService.import_from_oda(
                oda_product_id=oda_id_mock
            )

        assert Product.objects.all().count() == 1
        assert Product.objects.all().first().oda_id == imported_product.oda_id

        assert product_response_request_mock.call_count == 1
        assert product_image_response_request_mock.call_count == 1
        assert _validate_oda_response_mock.call_count == 1

    def test_import_from_oda_existing_product(
        self, django_assert_num_queries, request_mock, mocker, settings
    ):
        """
        Test that importing an existing product updates the product.
        """
        product = create_product(name="Some product name")
        oda_response = get_oda_product_response_dict(id=product.oda_id)

        product_response_request_mock = mocker.patch.object(
            OdaClient,
            "get_product",
            return_value=OdaProductDetailRecord(**oda_response),
        )
        product_image_response_request_mock = mocker.patch.object(
            OdaClient,
            "get_image",
            return_value=create_product_image(name="test"),
        )
        _validate_oda_response_mock = mocker.patch.object(
            ProductService, "_validate_oda_response"
        )

        with django_assert_num_queries(9):
            imported_product = ProductService.import_from_oda(
                oda_product_id=product.oda_id
            )

        assert imported_product.id == product.id
        assert imported_product.name == "Møllerens Hvetemel Siktet"
        assert imported_product.oda_id == oda_response["id"]
        assert imported_product.oda_id == product.oda_id

        assert product_response_request_mock.call_count == 1
        assert product_image_response_request_mock.call_count == 1
        assert _validate_oda_response_mock.call_count == 1
