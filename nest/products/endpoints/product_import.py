from django.http import HttpRequest
from ninja import Schema

from nest.api.responses import APIResponse
from nest.forms.fields import FormField
from nest.users.enums import AvatarColors

from .router import router


class TestSchemaOut(Schema):
    test: int


class TestSchemaIn(Schema):
    id: int = FormField(..., help_text="Hello")
    color: AvatarColors


@router.add_form("import/forms/", form=TestSchemaIn)
@router.post("import/", response={200: APIResponse[TestSchemaOut]})
def product_import_api(
    request: HttpRequest, payload: TestSchemaIn
) -> APIResponse[TestSchemaOut]:
    return APIResponse(status="success", data=TestSchemaOut(test=payload.id))
