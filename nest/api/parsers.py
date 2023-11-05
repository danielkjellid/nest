from typing import Any

import orjson
from django.http import HttpRequest
from ninja.parser import Parser
from store_kit.utils import decamelize, is_camelcase


class CamelCaseParser(Parser):
    """
    A parser that parses data from camel case to snake case,
    if the data sent is camel case. If not, it returns parsed
    data with orjson.
    """

    def parse_body(self, request: HttpRequest) -> Any:
        data = orjson.loads(request.body)

        if is_camelcase(data):
            decamelized_data = decamelize(data)
            return decamelized_data

        return data
