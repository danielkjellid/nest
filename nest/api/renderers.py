import decimal
from datetime import timedelta
from typing import Any

import orjson
from django.http import HttpRequest
from ninja.renderers import BaseRenderer
from store_kit.utils import camelize


def default(obj: Any) -> Any:
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    if isinstance(obj, timedelta):
        return obj.total_seconds()
    return obj


class CamelCaseRenderer(BaseRenderer):
    """
    Render that renders data as camel case, and uses orjson to parse it.
    """

    media_type = "application/json"

    def render(self, request: HttpRequest, data: Any, *, response_status: int) -> Any:
        camelized_data = camelize(data)
        return orjson.dumps(camelized_data, default=default)
