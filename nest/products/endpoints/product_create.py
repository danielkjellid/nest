from django.http import HttpRequest
from ninja import File, Form, Schema

from nest.api.fields import FormField
from nest.api.files import UploadedFile
from nest.api.responses import APIResponse
from nest.products.services import ProductService
from nest.frontend.components import FrontendComponents
from nest.core.decorators import staff_required

from .router import router


class ProductCreateIn(Schema):
    name: str = FormField(
        ...,
        help_text="Plain name of product, should not include unit.",
    )
    gross_price: str = FormField(
        ..., help_text="Gross price of product, including VAT."
    )
    unit_quantity: str = FormField(
        ...,
        help_text="Amount in selected unit type. E.g. 2 if 2 kg.",
        col_span=1,
    )
    unit_id: str = FormField(
        ...,
        alias="unit",
        help_text="What sort of unit is this?",
        col_span=1,
        component=FrontendComponents.SELECT.value,
    )
    supplier: str
    is_available: bool = FormField(..., default_value=True)

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

    ProductService.create_product(**payload.dict(), thumbnail=thumbnail)
    return APIResponse(status="success", data=None)
