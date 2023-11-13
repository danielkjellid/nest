from django.http import HttpRequest
from ninja import Router, Schema

from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.forms.fields import FormField

from .clients import OdaClient
from .services import import_product_from_oda

router = Router(tags=["Oda products"])


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


@router.post("import/", response=APIResponse[ProductOdaImportOut])
@staff_required
def product_oda_import_api(
    request: HttpRequest, payload: ProductOdaImportIn
) -> APIResponse[ProductOdaImportOut]:
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
            unit_quantity=str(
                float(response.gross_price) / float(response.gross_unit_price)
            ),
            thumbnail_url=response.images[0].thumbnail.url,
        ),
    )


class ProductOdaImportConfirmIn(Schema):
    oda_product_id: int


@router.post("import/confirm/", response=APIResponse[None])
@staff_required
def product_oda_import_confirm_api(
    request: HttpRequest, payload: ProductOdaImportConfirmIn
) -> APIResponse[None]:
    """
    Import and create a product from Oda based on ID.
    """
    import_product_from_oda(oda_product_id=payload.oda_product_id)
    return APIResponse(status="success", data=None)
