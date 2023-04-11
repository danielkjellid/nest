from django.http import HttpRequest

from nest.api.responses import APIResponse
from nest.selectors import ProductSelector

from .router import router
from ninja import Schema


class ProductListUnit(Schema):
    name: str
    abbreviation: str


class ProductList(Schema):
    id: int
    name: str
    supplier: str
    thumbnail_url: str | None
    is_available: bool
    oda_url: str | None
    oda_id: int | None
    gross_price: str
    gross_unit_price: str | None
    unit: ProductListUnit


@router.get("/", response={200: APIResponse[list[ProductList]]})
def product_list_api(request: HttpRequest) -> APIResponse[list[ProductList]]:
    """
    Get a list of all products in the application.
    """

    products = ProductSelector.all_products()
    data = [ProductList(**product.dict()) for product in products]

    return APIResponse(status="success", data=data)
