from decimal import Decimal
from typing import Any, Callable, TypedDict
from collections.abc import Mapping
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
def spec():
    def _spec(request_spec, default_spec):
        default_spec = default_spec.copy()

        if not request_spec or not isinstance(request_spec, dict):
            return default_spec

        def update_spec(
            original: dict[str, Any], new: dict[str, Any]
        ) -> dict[str, Any]:
            for key, value in new.items():
                if isinstance(value, Mapping):
                    original[key] = update_spec(original.get(key, {}), value)
                else:
                    original[key] = value
            return original

        return update_spec(default_spec, request_spec)

    return _spec


@pytest.fixture
def product_spec(
    request: pytest.FixtureRequest, spec, default_product_spec
) -> dict[str, Any]:
    request_spec = request.node.get_closest_marker("product").kwargs
    return spec(request_spec, default_product_spec)


@pytest.fixture
def create_product_from_spec(db: Any, get_unit: Callable[[str], Unit]):
    def _create_product(spec: dict[str, Any]):
        unit_abbreviation = spec.pop("unit")
        unit = get_unit(unit_abbreviation)
        product, _created = Product.objects.get_or_create(unit=unit, **spec)
        return product

    return _create_product


@pytest.fixture
def product(create_product_from_spec, product_spec):
    return create_product_from_spec(product_spec)


@pytest.fixture
def oda_product(create_product_from_spec, default_product_spec):
    modified_spec = default_product_spec.copy()
    modified_spec["oda_id"] = next_oda_id()
    modified_spec["oda_url"] = "https://example.com/"
    return create_product_from_spec(modified_spec)


@pytest.fixture
def products(
    request: pytest.FixtureRequest, spec, default_product_spec, create_product_from_spec
):
    products = {}

    for marker in request.node.iter_markers("products"):
        assert not marker.args, "Only kwargs is accepted with this fixture"

        for slug in marker.kwargs:
            request_spec = marker.kwargs.get(slug, {})
            products[slug] = create_product_from_spec(
                spec(request_spec, default_product_spec)
            )

    return products
