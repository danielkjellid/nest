from django.http import HttpRequest
from ninja import Schema, Form, File, UploadedFile

from nest.api.responses import APIResponse
from nest.units.enums import UnitType
from nest.forms.fields import FormField
from nest.core.files import UploadedFile
from nest.products.services import ProductService
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


class ProductAddThumbnailIn(ProductAddIn):
    thumbnail: UploadedFile


@router.add_form(
    "add/form/", form=ProductAddThumbnailIn, is_multipart_form=True, columns=2
)
@router.post("add/", response={200: APIResponse[None]})
def product_add_api(
    request: HttpRequest,
    payload: ProductAddIn = Form(...),
    thumbnail: UploadedFile = File(None),
) -> APIResponse[None]:
    created_product = ProductService.update_or_create_product(**payload.dict())
    print(created_product)
    return APIResponse(status="success", data={})
