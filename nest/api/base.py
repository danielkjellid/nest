from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI
from ninja.openapi.schema import OpenAPISchema
from ninja.security import django_auth

from .openapi import get_schema
from .parsers import CamelCaseParser
from .renderers import CamelCaseRenderer

if TYPE_CHECKING:
    from ninja.operation import Operation


class NestAPI(NinjaAPI):
    def __init__(self) -> None:
        super().__init__(
            title="Nest API",
            version="1.0.0",
            docs_decorator=staff_member_required,
            auth=django_auth,
            csrf=True,
            renderer=CamelCaseRenderer(),
            parser=CamelCaseParser(),
        )

    def get_openapi_schema(
        self,
        path_prefix: str | None = None,
        path_params: Any | None = None,
    ) -> OpenAPISchema:
        if path_prefix is None:
            path_prefix = self.get_root_path(path_params or {})
        return get_schema(api=self, path_prefix=path_prefix)

    def get_openapi_operation_id(self, operation: Operation) -> str:
        operation_id: str = operation.view_func.__name__
        return operation_id
