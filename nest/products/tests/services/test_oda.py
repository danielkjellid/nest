import pytest
from decimal import Decimal
from nest.data_pools.providers.oda.clients import OdaClient
from nest.data_pools.providers.oda.records import OdaProductDetailRecord
from nest.data_pools.tests.oda.utils import get_oda_product_response_dict
from nest.products.models import Product
from nest.products.constants import PRODUCT_NUTRITION_IDENTIFIERS
from nest.products.services import (
    import_from_oda,
)
from nest.products.services.oda import (
    _validate_oda_response,
    _extract_nutrition_values_from_response,
    _extract_classifier_values_from_response,
)
from nest.products.tests.utils import (
    create_product as create_product_test_util,
)
from nest.products.tests.utils import create_product_image

pytestmark = pytest.mark.django_db


class TestProductOdaServices:
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

        with django_assert_num_queries(11):
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

    def test__extract_nutrition_values_from_response(self):
        """
        Test that we're successfully extracting nutritional values from response and
        that all of our identifiers are a part of the returned dict.
        """
        product = create_product_test_util(name="Some product name")
        oda_response = get_oda_product_response_dict(id=product.oda_id)

        nutrition_values = _extract_nutrition_values_from_response(
            product_response=OdaProductDetailRecord(**oda_response)
        )

        assert nutrition_values == {
            "carbohydrates": Decimal("67.90"),
            "carbohydrates_polyols": None,
            "carbohydrates_starch": None,
            "carbohydrates_sugars": Decimal("2.70"),
            "energy_kcal": Decimal("338"),
            "energy_kj": Decimal("1433"),
            "fat": Decimal("1.60"),
            "fat_monounsaturated": Decimal("0.20"),
            "fat_polyunsaturated": Decimal("1"),
            "fat_saturated": Decimal("0.40"),
            "fibres": Decimal("3.60"),
            "protein": Decimal("11.20"),
            "salt": Decimal("0"),
            "sodium": None,
        }
        assert all(key in nutrition_values for key in PRODUCT_NUTRITION_IDENTIFIERS)

    def test__extract_classifier_values_from_response(self):
        """
        Test that we're successfully extracting classifier values from response.
        """
        product = create_product_test_util(name="Some product name")
        oda_response = get_oda_product_response_dict(id=product.oda_id)

        classifiers = _extract_classifier_values_from_response(
            product_response=OdaProductDetailRecord(**oda_response)
        )

        assert classifiers == {
            "allergens": "hvete",
            "ingredients": "Siktet mel av HVETE, melbehandlingsmiddel (ascorbinsyre)",
        }
