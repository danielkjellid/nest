from django.http import HttpRequest
from ninja import Schema

from nest.api.fields import FormField
from nest.api.responses import APIResponse
from nest.data_pools.providers.oda.clients import OdaClient

from .router import router


class ProductOdaImportOut(Schema):
    id: int
    full_name: str
    supplier: str | None
    is_available: bool
    gross_price: str
    unit: str
    unit_quantity: str
    thumbnail_url: str


class ProductOdaImportIn(Schema):
    oda_product_id: int = FormField(..., help_text="Product Id at Oda.")


@router.post("oda/import/", response=APIResponse[ProductOdaImportOut])
def product_oda_import_api(
    request: HttpRequest, payload: ProductOdaImportIn
) -> APIResponse[ProductOdaImportIn]:
    """
    Import product data from id. Note: This does not create a product, it only retrieves
    data.
    """
    response = OdaClient.get_product(product_id=payload.oda_product_id)

    return APIResponse(
        status="success",
        data=ProductOdaImportOut(
            id=response.id,
            full_name=response.full_name,
            supplier=response.brand,
            is_available=response.availability.is_available,
            gross_price=response.gross_price,
            unit=response.unit_price_quantity_abbreviation,
            unit_quantity=(
                float(response.gross_price) / float(response.gross_unit_price)
            ),
            thumbnail_url=response.images[0].thumbnail.url,
        ),
    )
