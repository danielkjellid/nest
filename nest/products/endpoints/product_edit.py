from decimal import Decimal

from django.http import HttpRequest
from ninja import File, Form, Schema

from nest.api.fields import FormField
from nest.api.files import UploadedFile
from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.frontend.components import FrontendComponents
from nest.products.services import edit_product

from .router import router


class ProductEditIn(Schema):
    name: str = FormField(
        ...,
        help_text="Plain name of product, should not include unit.",
    )
    gross_price: Decimal = FormField(
        ..., help_text="Gross price of product, including VAT."
    )
    unit_quantity: Decimal = FormField(
        ...,
        help_text="Amount in selected unit type. E.g. 2 if 2 kg.",
        col_span=1,
    )
    unit_id: int = FormField(
        ...,
        alias="unit",
        help_text="What sort of unit is this?",
        col_span=1,
        component=FrontendComponents.SELECT.value,
    )
    supplier: str
    gtin: str | None = FormField(
        None, help_text="Global trade item number. Number bellow barcode."
    )
    oda_id: int | None = FormField(None, help_text="Corresponding product id at Oda.")
    oda_url: str | None = FormField(None, help_text="Link to product at Oda.")
    is_available: bool = FormField(
        ..., help_text="Product is available and is actively used in recipes."
    )
    is_synced: bool = FormField(
        ..., help_text="Product is synced with external providers"
    )

    class FormMeta:
        columns = 2


@router.post("{product_id}/edit/", response=APIResponse[None])
@staff_required
def product_edit_api(
    request: HttpRequest,
    product_id: int,
    payload: ProductEditIn = Form(...),  # noqa
    thumbnail: UploadedFile | None = File(None),  # noqa
) -> APIResponse[None]:
    """
    Edit a product.
    """
    edit_product(
        request=request, product_id=product_id, thumbnail=thumbnail, **payload.dict()
    )
    return APIResponse(status="success", data=None)
