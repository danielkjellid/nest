from django.http import HttpRequest
from ninja import Schema

from nest.api.responses import APIResponse
from nest.products.services import get_product

from .router import router


class ProductDetailUnitOut(Schema):
    id: int
    name: str
    abbreviation: str
    unit_type: str
    display_name: str


class ProductDetailOut(Schema):
    id: int
    name: str
    full_name: str
    gross_price: str
    gross_unit_price: str | None
    unit: ProductDetailUnitOut
    unit_quantity: str | None
    oda_url: str | None
    oda_id: str | None
    is_available: bool
    thumbnail_url: str | None
    gtin: str | None
    supplier: str
    is_synced: bool


@router.get("{product_id}/", response=APIResponse[ProductDetailOut])
def product_detail_api(
    request: HttpRequest, product_id: int
) -> APIResponse[ProductDetailOut]:
    """
    Retrieve a single product instance based on product id.
    """
    product = get_product(pk=product_id)
    return APIResponse(status="success", data=ProductDetailOut(**product.dict()))
