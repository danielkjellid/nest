from django.http import HttpRequest
from ninja import Schema
from .utils import FormUtil
from typing import TypeVar, Any

S = TypeVar("S", bound=Schema)


def form_api(request: HttpRequest, **kwargs: Any) -> dict[str, Any]:
    """
    Form API is a generic class which returns a generated form from passed schema.
    Accessible through the @router.add_form(...) decorator.
    """
    form = FormUtil.create_form_from_schema(schema=kwargs["form"])
    return {"status": "success", "data": form}
