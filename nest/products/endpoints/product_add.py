from django.http import HttpRequest
from ninja import File, Form, Schema

from nest.api.fields import FormField
from nest.api.files import UploadedFile
from nest.api.responses import APIResponse
from nest.products.services import ProductService
from nest.units.enums import UnitType

from .router import router


class ProductAddIn(Schema):
    name: str = FormField(
        ...,
        help_text="Plain name of product, should not include unit.",
    )
    gross_price: str = FormField(
        ..., help_text="Gross price of product, including VAT."
    )
    unit: str = FormField(
        ...,
        help_text="Amount if product in selected unit type. E.g. 2 if 2 kg.",
        col_span=1,
    )
    unit_type: UnitType | str = FormField(..., col_span=1)
    supplier: str
    is_available: bool = FormField(..., default_value=True)

    class FormMeta:
        columns = 2


@router.post("add/", response={200: APIResponse[None]})
def product_add_api(
    request: HttpRequest,
    payload: ProductAddIn = Form(...),  # noqa
    thumbnail: UploadedFile = File(...),  # noqa
) -> APIResponse[None]:
    ProductService.update_or_create_product(**payload.dict())
    return APIResponse(status="success", data=None)
