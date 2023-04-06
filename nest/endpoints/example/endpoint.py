from ninja import Schema
from .router import router
from django.http import HttpRequest
from nest.api.responses import APIResponse


class TestSchema(Schema):
    id: int


@router.get("/", response={200: APIResponse[TestSchema]})
def example_api(request: HttpRequest):
    return APIResponse(status="success", data=TestSchema(id=1))
