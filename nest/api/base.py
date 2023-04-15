import re
from typing import Any, Iterable

from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI
from ninja.openapi.schema import OpenAPISchema

from nest.core.utils.humps import HumpsUtil

from .parsers import CamelCaseParser
from .renderers import CamelCaseRenderer


class NestAPI(NinjaAPI):
    def __init__(self) -> None:
        super().__init__(
            title="Nest API",
            version="1.0.0",
            docs_decorator=staff_member_required,
            # auth=django_auth,
            csrf=True,
            renderer=CamelCaseRenderer(),
            parser=CamelCaseParser(),
        )

    def _update_openapi_schema_reference(
        self,
        data: str | dict[str, Any] | OpenAPISchema | Iterable[Any],
        ref: str,
        updated_ref: str,
    ) -> Any:
        """
        Update a reference in the schema by recursive search and repalce.
        """
        if isinstance(data, str):
            return data.replace(ref, updated_ref)
        elif isinstance(data, dict):
            return {
                key: self._update_openapi_schema_reference(val, ref, updated_ref)
                for key, val in data.items()
            }
        elif isinstance(data, Iterable):
            return [
                self._update_openapi_schema_reference(val, ref, updated_ref)
                for val in data
            ]
        else:
            return data

    def _convert_openapi_schema_responses(self, schema: OpenAPISchema) -> OpenAPISchema:
        """
        Convert APIResponse generic type keys to an actual readable format as
        the automatic compiler struggles with generics.
        """
        component_schemas = schema["components"]["schemas"]

        for key, _value in component_schemas.copy().items():
            # Filter out keys with APIResponse prefix
            match = re.search("APIResponse", key)

            # We only care about keys with the substring APIResponse here, so if it
            # does not exist, continue to next iteration.
            if not match:
                continue

            # Split the key accordingly and formate as "SchemaAPIResponse".
            split_key: list[str] = list(filter(None, key.replace(".", "_").split("_")))
            formatted_key = f"{split_key[-1]}{split_key[0]}"

            component_schemas[formatted_key] = component_schemas.pop(key)
            component_schemas[formatted_key]["title"] = formatted_key
            schema = self._update_openapi_schema_reference(
                schema,
                f"#/components/schemas/{key}",
                f"#/components/schemas/{formatted_key}",
            )

        schema["components"]["schemas"] = component_schemas
        return schema

    @staticmethod
    def _convert_openapi_schema_to_camel_case(schema: OpenAPISchema) -> OpenAPISchema:
        """
        Convert schema components values to camelCase.
        """
        components = schema["components"]

        for key, value in components.copy().items():
            for schema_key, schema_value in value.items():
                components[key][schema_key] = HumpsUtil.camelize(schema_value)

        schema["components"] = components
        return schema

    def get_openapi_schema(self, path_prefix: str | None = None) -> OpenAPISchema:
        schema = super().get_openapi_schema(path_prefix=path_prefix)
        schema = self._convert_openapi_schema_responses(schema=schema)
        schema = self._convert_openapi_schema_to_camel_case(schema=schema)
        return schema
