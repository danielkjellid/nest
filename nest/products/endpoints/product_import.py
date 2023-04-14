from django.http import HttpRequest
from ninja import Schema
from .router import router


class TestSchemaOut(Schema):
    test: int


class TestSchemaIn(Schema):
    id: int


@router.add_form("import/forms/", form=TestSchemaIn)
@router.post("import/", response={200: TestSchemaOut})
def product_import_api(request: HttpRequest, payload: TestSchemaIn):
    return TestSchemaOut(test=payload.id)
