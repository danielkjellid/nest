from django.http import HttpRequest
from ninja import Schema, Router

from nest.api.responses import APIResponse
from nest.products.selectors import ProductSelector

from .router import router


class ProductListUnit(Schema):
    name: str
    abbreviation: str


class ProductList(Schema):
    id: int
    full_name: str
    supplier: str
    thumbnail_url: str | None
    is_available: bool
    oda_url: str | None
    oda_id: int | None
    gross_price: str
    gross_unit_price: str | None
    unit: ProductListUnit
    unit_quantity: str | None
    is_synced: bool
    last_synced_at: str | None


@router.get("/", response={200: APIResponse[list[ProductList]]})
def product_list_api(request: HttpRequest) -> APIResponse[list[ProductList]]:
    """
    Get a list of all products in the application.
    """

    products = ProductSelector.all_products()
    data = [ProductList(**product.dict()) for product in products]

    return APIResponse(status="success", data=data)
