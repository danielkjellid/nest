from decimal import Decimal
from typing import Any, Callable, TypedDict

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from nest.products.core.models import Product
from nest.units.models import Unit

from ..factories.fixtures import (
    get_instance,
    get_spec_for_instance,
    instance,
    instances,
)
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
def create_product(db: Any, get_unit: Callable[[str], Unit]) -> CreateProduct:
    """
    Creates a single product.

    This function does not provide any defaults, so everything needed has to be
    specified. You should probably use the get_product fixture instead.
    """

    def _create_product(spec: ProductSpec) -> Product:
        unit_abbreviation = spec.pop("unit")
        unit = get_unit(unit_abbreviation)
        product = Product.objects.create(unit=unit, **spec)

        return product

    return _create_product


@pytest.fixture
def default_product_spec(request: pytest.FixtureRequest) -> ProductSpec:
    """
    Get the default spec for a product.
    """

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
def get_product_spec(default_product_spec: ProductSpec, request: pytest.FixtureRequest):
    def _get_product_spec(slug: str) -> ProductSpec:
        return get_spec_for_instance(
            slug=slug,
            default_spec=default_product_spec,
            request=request,
            marker="products",
        )

    return _get_product_spec


@pytest.fixture
def get_product(
    create_product: CreateProduct,
    get_product_spec: Callable[[str], ProductSpec],
) -> Callable[[str], Product]:
    products: dict[str, Product] = {}

    def get_or_create_product(slug: str) -> Product:
        return get_instance(
            slug=slug,
            instances=products,
            create_callback=create_product,
            get_spec_callback=get_product_spec,
        )

    return get_or_create_product


@pytest.fixture
def product(
    request: pytest.FixtureRequest,
    create_product: CreateProduct,
    default_product_spec: ProductSpec,
) -> Product:
    return instance(
        create_callback=create_product,
        default_spec=default_product_spec,
        request=request,
        marker="product",
    )


@pytest.fixture
def oda_product(
    request: pytest.FixtureRequest,
    create_product: CreateProduct,
    default_product_spec: ProductSpec,
) -> Product:
    spec = default_product_spec.copy()
    spec.update({"oda_id": next_oda_id(), "oda_url": "https://example.com/"})

    return instance(
        create_callback=create_product,
        default_spec=spec,
        request=request,
        marker="oda_product",
    )


@pytest.fixture
def products(
    get_product: Callable[[str], Product], request: pytest.FixtureRequest
) -> dict[str, Product]:
    """
    Get all products provided as kwargs as
    """
    return instances(
        request=request, markers="products", get_instance_callback=get_product
    )
