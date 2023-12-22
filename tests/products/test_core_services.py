from decimal import Decimal
from typing import Any, Callable

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from nest.products.core.models import Product
from nest.products.core.services import (
    create_product,
    edit_product,
    update_or_create_product,
)
from nest.units.models import Unit

from .utils import next_oda_id


def test_service_create_product(
    get_unit: Callable[[str], Unit], django_assert_num_queries: Any
):
    """
    Test that create_product service successfully creates a product with expected
    output.
    """
    unit = get_unit("kg")
    initial_count = Product.objects.all().count()

    fields = {
        "gross_price": "140.20",
        "unit_id": unit.id,
        "unit_quantity": 2,
        "supplier": "Awesome supplier",
    }

    with django_assert_num_queries(5):
        product_no_thumbnail = create_product(
            name="Awesome product",
            **fields,
        )

    # A new product should have been created.
    assert Product.objects.all().count() == initial_count + 1

    assert product_no_thumbnail.name == "Awesome product"
    assert product_no_thumbnail.gross_price == Decimal("140.20")
    assert product_no_thumbnail.unit.id == unit.id
    assert product_no_thumbnail.unit_quantity == 2
    assert product_no_thumbnail.supplier == "Awesome supplier"
    assert product_no_thumbnail.is_oda_product is False
    assert product_no_thumbnail.gross_unit_price == Decimal("70.10")
    assert product_no_thumbnail.thumbnail_url is None

    with django_assert_num_queries(5):
        product = create_product(
            name="Another awesome product",
            thumbnail=SimpleUploadedFile("thump.jpg", b"", content_type="image/jpeg"),
            **fields,
        )

    assert Product.objects.all().count() == initial_count + 2
    assert product.name == "Another awesome product"
    assert product.thumbnail_url is not None


@pytest.mark.product(
    name="A cool product", supplier="A cool supplier", unit="g", oda_id=None
)
def test_service_edit_product(
    product: Product,
    get_unit: Callable[[str], Unit],
    django_assert_max_num_queries: Any,
) -> None:
    """
    Test that the edit_product service edits a product within query limits.
    """

    unit_kg = get_unit("kg")
    with django_assert_max_num_queries(7):
        updated_product = edit_product(
            product_id=product.id, name="Wubadubadub", unit_id=unit_kg.id
        )

    assert updated_product.id == product.id
    assert updated_product.name == "Wubadubadub"
    assert updated_product.unit.id == unit_kg.id
    assert updated_product.supplier == "A cool supplier"


@pytest.mark.product(name="Test product", oda_id=None)
def test_service_update_or_create_product_with_pk(
    product: Product,
    get_unit: Callable[[str], Unit],
    django_assert_num_queries: Any,
) -> None:
    """
    Test that the update_or_create_product creates or updates as expected.
    """
    unit = get_unit("g")
    defaults = {
        "name": "New example product",
        "gross_price": Decimal("50.00"),
        "gross_unit_price": Decimal("50.00"),
        "unit_id": unit.id,
        "unit_quantity": Decimal("1.00"),
        "is_available": True,
        "supplier": "Test supplier",
    }

    initial_count = Product.objects.all().count()

    # Test that creating a product works as expected.
    with django_assert_num_queries(6):
        update_or_create_product(**defaults)

    # One new product should have been created.
    assert Product.objects.all().count() == initial_count + 1

    existing_product = product
    assert existing_product.name == "Test product"

    defaults = {
        "name": "Updated test product",
        "gross_price": existing_product.gross_price,
        "gross_unit_price": existing_product.gross_unit_price,
        "unit_id": existing_product.unit_id,
        "unit_quantity": existing_product.unit_quantity,
        "is_available": existing_product.is_available,
        "supplier": existing_product.supplier,
    }

    # Test that updating existing product works as expected.
    with django_assert_num_queries(4):
        updated_product = update_or_create_product(pk=existing_product.id, **defaults)

    # No new objects should have been created this time.
    assert Product.objects.all().count() == initial_count + 1

    assert updated_product.id == existing_product.id
    assert updated_product.name == "Updated test product"


@pytest.mark.oda_product(name="Test product")
def test_service_test_update_or_create_product_with_oda_id(
    oda_product: Product,
    get_unit: Callable[[str], Unit],
    django_assert_num_queries: Any,
) -> None:
    """
    Test that update or create with oda id correctly updates or creates as expected.
    """
    unit = get_unit("g")
    defaults = {
        "name": "New example product",
        "gross_price": Decimal("50.00"),
        "gross_unit_price": Decimal("50.00"),
        "unit_id": unit.id,
        "unit_quantity": Decimal("1.00"),
        "is_available": True,
        "supplier": "Test supplier",
    }

    initial_count = Product.objects.all().count()

    # Test that creating a product works as expected.
    with django_assert_num_queries(6):
        update_or_create_product(oda_id=next_oda_id(), **defaults)

    # One new product should have been created.
    assert Product.objects.all().count() == initial_count + 1
    existing_product = oda_product
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

    assert existing_product.oda_id is not None

    with django_assert_num_queries(4):
        updated_product = update_or_create_product(
            oda_id=existing_product.oda_id, **defaults
        )

    # No new objects should have been created this time.
    assert Product.objects.all().count() == initial_count + 1

    assert updated_product.id == existing_product.id
    assert updated_product.name == "Updated test product"
    assert updated_product.oda_id == existing_product.oda_id
