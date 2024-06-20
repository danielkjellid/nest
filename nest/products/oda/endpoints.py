from django.http import HttpRequest
from ninja import Router, Schema
from store_kit.http import status

from nest.api.responses import APIResponse
from nest.core.decorators import staff_required

from .forms import ProductOdaImportForm
from .records import OdaProductDetailRecord
from .selectors import retrieve_product_from_oda
from .services import import_product_from_oda

router = Router(tags=["Oda products"])


class ProductOdaImportOut(Schema):
    product: OdaProductDetailRecord
    has_been_imported_previously: bool


@router.post("import/", response=APIResponse[ProductOdaImportOut])
@staff_required
def product_oda_import_api(
    request: HttpRequest, payload: ProductOdaImportForm
) -> APIResponse[ProductOdaImportOut]:
    """
    Import product data from id. Note: This does not create a product, it only retrieves
    data.
    """
    oda_product, is_imported = retrieve_product_from_oda(
        oda_product_id=payload.oda_product_id
    )
    return APIResponse(
        status="success",
        data=ProductOdaImportOut(
            product=oda_product,
            has_been_imported_previously=is_imported,
        ),
    )


class ProductOdaImportConfirmIn(Schema):
    oda_product_id: int


@router.post("import/confirm/", response={201: APIResponse[None]})
@staff_required
def product_oda_import_confirm_api(
    request: HttpRequest, payload: ProductOdaImportConfirmIn
) -> tuple[int, APIResponse[None]]:
    """
    Import and create a product from Oda based on ID.
    """
    import_product_from_oda(oda_product_id=payload.oda_product_id)
    return status.HTTP_201_CREATED, APIResponse(status="success", data=None)
