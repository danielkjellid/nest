from typing import Any

from django.http import HttpRequest

from .form import Form


def form_api(request: HttpRequest, **kwargs: Any) -> dict[str, Any]:
    """
    Form API is a generic class which returns a generated form from passed schema.
    Accessible through the @router.add_form(...) decorator.
    """
    form = Form.create_from_schema(
        schema=kwargs["form"],
        is_multipart_form=kwargs["is_multipart_form"],
        columns=kwargs["columns"],
    )
    return {"status": "success", "data": form}