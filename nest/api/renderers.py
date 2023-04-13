from typing import Any

import orjson
from django.http import HttpRequest
from ninja.renderers import BaseRenderer

from nest.core.utils.humps import HumpsUtil


class CamelCaseRenderer(BaseRenderer):
    """
    Render that renders data as camel case, and uses orjson to parse it.
    """

    media_type = "application/json"

    def render(self, request: HttpRequest, data: Any, *, response_status: int) -> Any:
        camelized_data = HumpsUtil.camelize(data)
        return orjson.dumps(camelized_data)
