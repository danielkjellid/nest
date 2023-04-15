from django.http import HttpRequest
from ninja import Schema

from nest.forms.fields import FormField
from nest.api.responses import APIResponse
from pydantic import Field
from .router import router


class TestSchemaOut(Schema):
    test: int


class TestSchemaIn(Schema):
    id: int = FormField(..., help_text="Hello")


@router.add_form("import/forms/", form=TestSchemaIn)
@router.post("import/", response={200: APIResponse[TestSchemaOut]})
def product_import_api(
    request: HttpRequest, payload: TestSchemaIn
) -> APIResponse[TestSchemaOut]:
    return APIResponse(status="success", data=TestSchemaOut(test=payload.id))
