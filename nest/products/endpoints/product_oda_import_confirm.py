from django.http import HttpRequest
from ninja import Schema
from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.products.services import import_from_oda

from .router import router


class ProductOdaImportConfirmIn(Schema):
    oda_product_id: int


@router.post("oda/import/confirm/", response=APIResponse[None])
@staff_required
def product_oda_import_confirm_api(
    request: HttpRequest, payload: ProductOdaImportConfirmIn
) -> APIResponse[None]:
    """
    Import and create a product from Oda based on ID.
    """
    import_from_oda(oda_product_id=payload.oda_product_id)
    return APIResponse(status="success", data=None)
