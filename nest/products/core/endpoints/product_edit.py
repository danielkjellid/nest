from decimal import Decimal

from django.http import HttpRequest
from ninja import File, Form, Schema

from nest.api.fields import FormField
from nest.api.files import UploadedFile
from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.frontend.components import FrontendComponents
from nest.products.core.services import edit_product

from .router import router


class ProductEditIn(Schema):
    name: str = FormField(
        ...,
        order=1,
        help_text="Plain name of product, should not include unit.",
    )
    gross_price: Decimal = FormField(
        ..., order=2, help_text="Gross price of product, including VAT."
    )
    unit_quantity: Decimal = FormField(
        ...,
        order=3,
        help_text="Amount in selected unit type. E.g. 2 if 2 kg.",
        col_span=2,
    )
    unit_id: int = FormField(
        ...,
        alias="unit",
        order=4,
        help_text="What sort of unit is this?",
        col_span=2,
        component=FrontendComponents.SELECT.value,
    )
    supplier: str = FormField(..., order=5)
    gtin: str | None = FormField(
        None,
        order=6,
        help_text="Global trade item number. Number bellow barcode.",
    )
    oda_id: int | None = FormField(
        None, order=7, help_text="Corresponding product id at Oda."
    )
    oda_url: str | None = FormField(None, order=8, help_text="Link to product at Oda.")
    fat: str | None = FormField(None, order=9, col_span=1)
    fat_saturated: str | None = FormField(None, order=10, col_span=1)
    fat_monounsaturated: str | None = FormField(None, order=11, col_span=1)
    fat_polyunsaturated: str | None = FormField(None, order=12, col_span=1)
    carbohydrates: str | None = FormField(None, order=13, col_span=1)
    carbohydrates_sugars: str | None = FormField(None, order=14, col_span=1)
    carbohydrates_polyols: str | None = FormField(None, order=15, col_span=1)
    carbohydrates_starch: str | None = FormField(None, order=16, col_span=1)
    fibres: str | None = FormField(None, order=17, col_span=4)
    salt: str | None = FormField(None, order=18, col_span=4)
    sodium: str | None = FormField(None, order=19, col_span=4)
    is_available: bool = FormField(
        ...,
        order=20,
        help_text="Product is available and is actively used in recipes.",
    )
    is_synced: bool = FormField(
        ...,
        order=21,
        help_text="Product is synced with external providers",
    )

    class FormMeta:
        columns = 4


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
