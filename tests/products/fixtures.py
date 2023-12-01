import pytest
from nest.products.core.models import Product
from typing import Any, TypedDict, Callable
from decimal import Decimal
from nest.units.models import Unit


class ProductSpec(TypedDict, total=False):
    name: str
    unit: str


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
def default_product_spec(
    get_unit: Callable[[str], Unit], request: pytest.FixtureRequest
) -> ProductSpec:
    """
    Get the default spec for a product.
    """

    # Default product data
    return {
        "name": "Sample product",
        "gross_price": Decimal("100"),
        "gross_unit_price": Decimal("100"),
        "unit": "kg",
        "unit_quantity": "1",
        "is_available": True,
        "thumbnail": None,
        "gtin": None,
        "supplier": "Sample supplier",
        "ingredients": None,
        "allergens": None,
        "contains_gluten": False,
        "contains_lactose": False,
    }


@pytest.fixture
def get_product_spec(default_product_spec: ProductSpec, request: pytest.FixtureRequest):
    def _get_product_spec(slug: str) -> ProductSpec:
        spec = default_product_spec.copy()

        if marker := request.node.get_closest_marker("products"):
            spec.update(marker.kwargs.get(slug, {}))

        return spec

    return _get_product_spec


@pytest.fixture
def get_product(
    create_product: Callable[[ProductSpec], Product],
    get_product_spec: Callable[[str], ProductSpec],
) -> Callable[[str], Product]:
    products: dict[str, Product] = {}

    def get_or_create_product(slug: str) -> Product:
        if product := products.get(slug):
            return product

        spec = get_product_spec(slug)
        product = create_product(spec)
        products[slug] = product
        return product

    return get_or_create_product


@pytest.fixture
def product(
    request: pytest.FixtureRequest,
    create_product: CreateProduct,
    default_product_spec: ProductSpec,
) -> Product:
    spec = default_product_spec.copy()

    marker = request.node.get_closest_marker("product")
    if marker:
        spec.update(marker.kwargs)

    return create_product(spec)


@pytest.fixture(autouse=True)
def products(get_product, request: pytest.FixtureRequest) -> dict[str, Product]:
    """
    Get all products provided as kwargs as
    """
    products: dict[str, ProductSpec] = {}

    for marker in request.node.iter_markers("products"):
        assert not marker.args, "Only kwargs is accepted with this fixture"
        slugs = marker.kwargs

        for slug in slugs:
            products.update({slug: get_product(slug)})

    for name, spec in products.items():
        if name in request.node.fixturenames:
            request.node.funcargs.setdefault(name, spec)

    return products
