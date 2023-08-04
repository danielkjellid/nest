from django.http import HttpRequest
from ninja import File, Form, Schema

from nest.api.fields import FormField
from nest.api.files import UploadedFile
from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.frontend.components import FrontendComponents
from nest.products.services import create_product

from .router import router


class ProductCreateIn(Schema):
    name: str = FormField(
        ...,
        order=1,
        help_text="Plain name of product, should not include unit.",
    )
    gross_price: str = FormField(
        ..., order=2, help_text="Gross price of product, including VAT."
    )
    unit_quantity: str = FormField(
        ...,
        order=3,
        help_text="Amount in selected unit type. E.g. 2 if 2 kg.",
        col_span=1,
    )
    unit_id: int = FormField(
        ...,
        alias="unit",
        help_text="What sort of unit is this?",
        col_span=1,
        order=4,
        component=FrontendComponents.SELECT.value,
    )
    supplier: str = FormField(..., order=5)
    gtin: str | None = FormField(None, order=6)
    ingredients: str | None = FormField(
        None,
        order=7,
        help_text="Specify ingredients seperated by a comma. E.g. milk, egg, sugar.",
        component=FrontendComponents.TEXT_AREA.value,
    )
    allergens: str | None = FormField(
        None,
        order=8,
        help_text="Specify allergens seperated by a comma. E.g. milk, egg, sugar.",
        component=FrontendComponents.TEXT_AREA.value,
    )
    fat: str | None = FormField(None, order=9, col_span=1)
    fat_saturated: str | None = FormField(None, order=10, col_span=1)
    fat_monounsaturated: str | None = FormField(None, order=11, col_span=1)
    fat_polyunsaturated: str | None = FormField(None, order=12, col_span=1)
    carbohydrates: str | None = FormField(None, order=13, col_span=1)
    carbohydrates_sugars: str | None = FormField(None, order=14, col_span=1)
    carbohydrates_polyols: str | None = FormField(None, order=15, col_span=1)
    carbohydrates_starch: str | None = FormField(None, order=16, col_span=1)
    fibres: str | None = FormField(None, order=17, col_span=2)
    salt: str | None = FormField(None, order=18, col_span=2)
    sodium: str | None = FormField(None, order=19, col_span=2)
    is_available: bool = FormField(..., order=20, default_value=True)

    class FormMeta:
        columns = 2


@router.post("create/", response=APIResponse[None])
@staff_required
def product_create_api(
    request: HttpRequest,
    payload: ProductCreateIn = Form(...),  # noqa
    thumbnail: UploadedFile | None = File(None),  # noqa
) -> APIResponse[None]:
    """
    Create a normal product.
    """

    create_product(**payload.dict(), thumbnail=thumbnail)
    return APIResponse(status="success", data=None)
