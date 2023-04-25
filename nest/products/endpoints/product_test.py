from .router import router
from nest.api.responses import APIResponse
from ninja import Schema
from nest.forms.fields import FormField


class TestSchema(Schema):
    id: str = FormField(..., help_text="Testing")
    name_lastname: str = FormField(..., placeholder="Test")


@router.post("test/", response=APIResponse[None])
def product_test_api(request, payload: TestSchema):
    return APIResponse(status="success", data={})
