from django.http import HttpRequest
from ninja import Schema
from .utils import FormUtil
from typing import TypeVar, Any


class Random(Schema):
    id: int
    name: str


S = TypeVar("S", bound=Schema)


def form_api(request: HttpRequest):
    print("called")
    f = FormUtil.create_form_from_schema(schema=Random)
    return 200, f
