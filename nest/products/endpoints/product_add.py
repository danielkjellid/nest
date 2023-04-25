import json

from django.http import HttpRequest
from ninja import Schema, Form, File, UploadedFile
from django.core.serializers.json import DjangoJSONEncoder

from nest.api.responses import APIResponse
from nest.units.enums import UnitType
from nest.forms.fields import FormField
from nest.core.files import UploadedFile
from nest.forms.form import Form as NForm
from nest.products.services import ProductService
from .router import router

forms = []


def create_form(decorated_class):
    init = decorated_class.__init__
    print("called")

    def __init__(self, *args, **kwargs):
        init(self, *args, **kwargs)
        self.__annotations__.update(
            {"form": NForm.create_from_schema(schema=decorated_class)}
        )

    decorated_class.__init__ = __init__
    return decorated_class


@create_form
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


# @router.add_form(
#     "add/form/", form=ProductAddThumbnailIn, is_multipart_form=True, columns=2
# )


@router.post(
    "add/",
    response={200: APIResponse[None]},
    openapi_extra={
        "requestBody": {
            "content": {"multipart/form-data": {"schema": {"title": "ProductAddIn"}}}
        }
    },
)
def product_add_api(
    request: HttpRequest,
    payload: ProductAddIn = Form(...),
    thumbnail: UploadedFile = File(None),
) -> APIResponse[None]:
    created_product = ProductService.update_or_create_product(**payload.dict())
    print(created_product)
    return APIResponse(status="success", data={})
