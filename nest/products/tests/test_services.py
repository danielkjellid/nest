from decimal import Decimal

import pytest

from nest.data_pools.providers.oda.clients import OdaClient
from nest.data_pools.providers.oda.records import OdaProductDetailRecord
from nest.data_pools.tests.oda.utils import get_oda_product_response_dict
from nest.products.models import Product
from nest.products.services import (
    _validate_oda_response,
    create_product,
    edit_product,
    import_from_oda,
    update_or_create_product,
)
from nest.products.tests.utils import (
    create_product as create_product_test_util,
)
from nest.products.tests.utils import (
    create_product_image,
    get_unit,
    next_oda_id,
)

pytestmark = pytest.mark.django_db


class TestProductServices:
    def test_create_product(self, django_assert_num_queries):
        """
        Test that create_product service successfully creates a product with expected
        output.
        """
        unit = get_unit(abbreviation="kg")
        assert Product.objects.count() == 0

        fields = {
            "gross_price": "140.20",
            "unit_id": unit.id,
            "unit_quantity": 2,
            "supplier": "Awesome supplier",
        }

        with django_assert_num_queries(3):
            product_no_thumbnail = create_product(
                name="Awesome product",
                **fields,
            )

        assert Product.objects.count() == 1

        assert product_no_thumbnail.name == "Awesome product"
        assert product_no_thumbnail.gross_price == Decimal("140.20")
        assert product_no_thumbnail.unit.id == unit.id
        assert product_no_thumbnail.unit_quantity == 2
        assert product_no_thumbnail.supplier == "Awesome supplier"
        assert product_no_thumbnail.is_oda_product is False
        assert product_no_thumbnail.gross_unit_price == Decimal("70.10")
        assert product_no_thumbnail.thumbnail_url is None

        with django_assert_num_queries(3):
            product = create_product(
                name="Another awesome product",
                thumbnail=create_product_image(name="thumb"),
                **fields,
            )

        assert Product.objects.count() == 2

        assert product.name == "Another awesome product"
        assert product.thumbnail_url is not None

    def test_edit_product(self, django_assert_num_queries):
        """
        Test that the edit_product service edits a product within query limits.
        """

        unit_kg = get_unit(abbreviation="kg")
        unit_g = get_unit(abbreviation="g")
        product = create_product_test_util(
            name="A cool product", supplier="A cool supplier", unit=unit_g
        )

        with django_assert_num_queries(8):
            updated_product = edit_product(
                product_id=product.id, name="Wubadubadub", unit_id=unit_kg.id
            )

        assert updated_product.id == product.id
        assert updated_product.name == "Wubadubadub"
        assert updated_product.unit.id == unit_kg.id
        assert updated_product.supplier == "A cool supplier"

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

        with django_assert_num_queries(8):
            update_or_create_product(**defaults)

        assert Product.objects.all().count() == 1

        existing_product = create_product_test_util()
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

        with django_assert_num_queries(9):
            updated_product = update_or_create_product(
                pk=existing_product.id, **defaults
            )

        assert updated_product.id == existing_product.id
        assert updated_product.name == "Updated test product"

    def test_update_or_create_product_with_oda_id(self, django_assert_num_queries):
        """ """
        existing_product = create_product_test_util()
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

        with django_assert_num_queries(9):
            updated_product = update_or_create_product(
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
        product = create_product_test_util(is_synced=False)
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
        _validate_oda_response_mock = mocker.patch(
            f"{_validate_oda_response.__module__}.{_validate_oda_response.__name__}"
        )

        with django_assert_num_queries(1):
            imported_product = import_from_oda(oda_product_id=product.oda_id)

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
        _validate_oda_response_mock = mocker.patch(
            f"{_validate_oda_response.__module__}.{_validate_oda_response.__name__}"
        )

        with django_assert_num_queries(10):
            imported_product = import_from_oda(oda_product_id=oda_id_mock)

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
        product = create_product_test_util(name="Some product name")
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
        _validate_oda_response_mock = mocker.patch(
            f"{_validate_oda_response.__module__}.{_validate_oda_response.__name__}"
        )

        with django_assert_num_queries(11):
            imported_product = import_from_oda(oda_product_id=product.oda_id)

        assert imported_product.id == product.id
        assert imported_product.name == "Møllerens Hvetemel Siktet"
        assert imported_product.oda_id == oda_response["id"]
        assert imported_product.oda_id == product.oda_id

        assert product_response_request_mock.call_count == 1
        assert product_image_response_request_mock.call_count == 1
        assert _validate_oda_response_mock.call_count == 1
