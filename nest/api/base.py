from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI
from ninja.openapi.schema import OpenAPISchema
from ninja.security import django_auth
from .openapi import get_schema
from .parsers import CamelCaseParser
from .renderers import CamelCaseRenderer


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

    def get_openapi_schema(self, path_prefix: str | None = None) -> OpenAPISchema:
        if path_prefix is None:
            path_prefix = self.root_path
        return get_schema(api=self, path_prefix=path_prefix)

    def get_openapi_operation_id(self, operation: "Operation") -> str:
        return operation.view_func.__name__
