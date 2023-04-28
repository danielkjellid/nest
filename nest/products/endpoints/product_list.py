from django.http import HttpRequest
from ninja import Schema

from nest.api.responses import APIResponse
from nest.products.selectors import ProductSelector

from .router import router


class ProductListOut(Schema):
    id: int
    full_name: str
    thumbnail_url: str | None
    is_available: bool
    oda_url: str | None
    oda_id: int | None
    is_synced: bool
    gtin: str | None
    is_oda_product: bool
    display_price: str


@router.get("/", response=APIResponse[list[ProductListOut]])
def product_list_api(request: HttpRequest) -> APIResponse[list[ProductListOut]]:
    """
    Get a list of all products in the application.
    """
    products = ProductSelector.all_products()
    data = [ProductListOut(**product.dict()) for product in products]

    return APIResponse(status="success", data=data)
