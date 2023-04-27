from django.http import HttpRequest
from ninja import Schema

from nest.api.responses import APIResponse
from nest.api.fields import FormField
from nest.data_pools.providers.oda.clients import OdaClient
from .router import router


class ProductImportOut(Schema):
    id: int
    name: str
    oda_url: str
    gross_price: str


class ProductImportIn(Schema):
    oda_product_id: str = FormField(..., help_text="Product Id at Oda.")


@router.post("import/", response=APIResponse[ProductImportOut])
def product_import_api(
    request: HttpRequest, payload: ProductImportIn
) -> APIResponse[ProductImportOut]:
    response = OdaClient.get_product(product_id=payload.oda_product_id)

    return APIResponse(
        status="success",
        data=ProductImportOut(
            id=response.id,
            name=response.full_name,
            oda_url=response.front_url,
            gross_price=response.gross_price,
        ),
    )
