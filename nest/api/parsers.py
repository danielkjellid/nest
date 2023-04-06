from typing import Any
from django.http import HttpRequest
import orjson

from ninja.parser import Parser
from nest.utils import HumpsUtil


class CamelCaseParser(Parser):
    """
    A parser that parses data from camel case to snake case,
    if the data sent is camel case. If not, it returns parsed
    data with orjson.
    """

    def parse_body(self, request: HttpRequest) -> Any:
        data = orjson.loads(request.body)

        if HumpsUtil.is_camelcase(data):
            decamelized_data = HumpsUtil.decamelize(data)
            return decamelized_data

        return data
