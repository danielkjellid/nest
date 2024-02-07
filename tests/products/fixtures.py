from decimal import Decimal
from typing import Any, Callable, TypedDict

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from nest.products.core.models import Product
from nest.units.models import Unit

from .utils import next_oda_id


class ProductSpec(TypedDict, total=False):
    name: str
    oda_id: int | None
    oda_url: str | None
    gross_price: Decimal
    gross_unit_price: Decimal
    unit: str
    unit_quantity: Decimal
    is_available: bool
    thumbnail: SimpleUploadedFile | None
    gtin: str | None
    supplier: str
    ingredients: str | None
    allergens: str | None
    contains_gluten: bool
    contains_lactose: bool


CreateProduct = Callable[[ProductSpec], Product]


@pytest.fixture
def default_product_spec() -> ProductSpec:
    return ProductSpec(
        name="Sample product",
        oda_id=None,
        oda_url=None,
        gross_price=Decimal("100"),
        gross_unit_price=Decimal("100"),
        unit="kg",
        unit_quantity="1",
        is_available=True,
        thumbnail=None,
        gtin=None,
        supplier="Sample supplier",
        ingredients=None,
        allergens=None,
        contains_gluten=False,
        contains_lactose=False,
    )


@pytest.fixture
def create_product_from_spec(db: Any, get_unit: Callable[[str], Unit]) -> CreateProduct:
    def _create_product(spec: ProductSpec) -> Product:
        unit_abbreviation = spec.pop("unit")
        unit = get_unit(unit_abbreviation)
        product, _created = Product.objects.get_or_create(unit=unit, **spec)
        return product

    return _create_product


@pytest.fixture
def product(create_instance, create_product_from_spec, default_product_spec) -> Product:
    return create_instance(
        create_callback=create_product_from_spec,
        default_spec=default_product_spec,
        marker_name="product",
    )


@pytest.fixture
def oda_product(
    create_instance, create_product_from_spec, default_product_spec
) -> Product:
    modified_spec = default_product_spec.copy()
    modified_spec["oda_id"] = next_oda_id()
    modified_spec["oda_url"] = "https://example.com/"

    return create_instance(
        create_callback=create_product_from_spec,
        default_spec=modified_spec,
        marker_name="oda_product",
    )


@pytest.fixture
def products(
    create_instances, default_product_spec, create_product_from_spec
) -> dict[str, Product]:
    return create_instances(
        create_callback=create_product_from_spec,
        default_spec=default_product_spec,
        marker_name="products",
    )
