from ninja.openapi.schema import (
    OpenAPISchema,
    BODY_CONTENT_TYPES,
    merge_schemas,
    REF_PREFIX,
)
from pydantic.schema import enum_process_schema
from django.conf import settings
from pydantic import BaseModel
from pydantic.schema import model_schema
import inspect
from ninja import NinjaAPI
from typing import Any, Type, cast, get_type_hints, get_args, Union, Iterable
from enum import Enum
from nest.core.files import UploadedFile, UploadedImageFile
from nest.core.utils.humps import HumpsUtil
from django.db.models import TextChoices, IntegerChoices

MANUALLY_ADDED_SCHEMAS = []


def add_to_openapi_schema(decorated_class: Any):
    """
    Decorator that can be used to manually add schemas, basemodels and enums to
    generated openapi schema.
    """
    MANUALLY_ADDED_SCHEMAS.append(decorated_class)
    return decorated_class


def get_schema(api: NinjaAPI, path_prefix: str = "") -> OpenAPISchema:
    openapi = OpenAPISchema(api, path_prefix)
    return openapi


class OpenAPISchema(OpenAPISchema):
    @staticmethod
    def _format_enum_from_type(typ: Any) -> list[dict[str, str | int]] | None:
        """
        Format schema field's enum type into a key - value format, taking advantage
        of Django's human-readable labels where applicable.
        """

        type_to_check = typ
        args_iterable = get_args(typ)

        if args_iterable:
            type_to_check = next(
                (
                    item
                    for item in args_iterable
                    if inspect.isclass(item) and issubclass(item, Enum)
                ),
                None,
            )

            if not type_to_check:
                return None

        # If passed enum is a django choices field, we can take advantaged
        # of the defined label.
        if issubclass(type_to_check, IntegerChoices | TextChoices):
            return [
                {"label": item.label, "value": item.value} for item in type_to_check
            ]
        elif issubclass(type_to_check, Enum):
            return [
                {"label": item.name.replace("_", " ").title(), "value": item.value}
                for item in type_to_check
            ]

        return None

    def _extract_enum_from_models(
        self, models
    ) -> dict[str, list[dict[str, str | int]]]:
        enum_mapping = []

        for model in models:
            for key, val in model.__fields__.items():
                for field_name, type_ in get_type_hints(val.type_).items():
                    enum = self._format_enum_from_type(typ=type_)

                    if enum:
                        enum_mapping.append(
                            {
                                "field": field_name,
                                "enum": self._format_enum_from_type(typ=type_),
                            }
                        )

        return enum_mapping

    def _populate_request_body_form_properties(
        self,
        properties: dict[str, Any],
        enum_mapping: dict[str, list[dict[str, str | int]]],
    ):
        props = self._convert_keys_to_camelcase(properties.copy())

        for property, property_value in props.items():
            property_type = property_value.get("type", None)
            for _key, _value in property_value.copy().items():
                for mapping in enum_mapping:
                    if mapping["field"] == property:
                        props[property]["enum"] = mapping["enum"]
                        props[property][
                            "component"
                        ] = settings.FORM_COMPONENT_MAPPING_DEFAULTS["enum"].value

                if (
                    property_type
                    # and property_type != "null"
                    and props[property].get("component", None) is None
                ):
                    try:
                        props[property][
                            "component"
                        ] = settings.FORM_COMPONENT_MAPPING_DEFAULTS[
                            property_value["type"]
                        ].value
                    except KeyError:
                        pass

        return HumpsUtil.camelize(props)

    def _convert_keys_to_camelcase(self, data: dict | list | None):
        if isinstance(data, dict):
            return {
                key: self._convert_keys_to_camelcase(val) for key, val in data.items()
            }
        elif isinstance(data, list):
            return [HumpsUtil.camelize(val) for val in data]
        else:
            return data

    def _update_schema(self, models, schema):
        # raise ValueError("i")
        mapped_enums = self._extract_enum_from_models(models=models)
        meta = self._set_schema_meta(models=models)

        schema_title_key, schema_val = next(iter(schema.items()))
        properties = schema_val.pop("properties", None)
        required = schema_val.pop("required", None)

        meta_title = meta.get("title", schema_title_key)

        updated_schema = {
            meta_title: {
                "title": meta_title,
                "properties": self._populate_request_body_form_properties(
                    properties=properties, enum_mapping=mapped_enums
                ),
                "required": self._convert_keys_to_camelcase(required),
                **meta,
                **schema_val,
            }
        }

        return updated_schema

    @staticmethod
    def _set_schema_meta(models) -> dict[str, any]:
        meta = {}

        for model in models:
            for key, value in get_type_hints(model).items():
                if issubclass(value, UploadedFile | UploadedImageFile):
                    continue

                meta["title"] = f"{value.__name__}"

                if hasattr(value, "FormMeta"):
                    meta["columns"] = getattr(value.FormMeta, "columns", 1)

        return meta

    def _create_schema_from_model(
        self, model, by_alias: bool = True, remove_level: bool = True
    ):
        if hasattr(model, "_flatten_map"):
            schema = self._flatten_schema(model)
        else:
            schema = model_schema(
                cast(Type[BaseModel], model), ref_prefix=REF_PREFIX, by_alias=by_alias
            )

        # move Schemas from definitions
        if schema.get("definitions"):
            definitions = schema.pop("definitions")
            updated_schema = self._update_schema(schema=definitions, models=[model])
            self.add_schema_definitions(updated_schema)

        if remove_level and len(schema["properties"]) == 1:
            name, details = list(schema["properties"].items())[0]

            # ref = details["$ref"]
            required = name in schema.get("required", {})
            return details, required
        else:
            return schema, True

    def _create_multipart_schema_from_models(self, models) -> tuple[Any, str]:
        # We have File and Form or Body, so we need to use multipart (File)
        content_type = BODY_CONTENT_TYPES["file"]

        result = merge_schemas(
            [
                self._create_schema_from_model(model, remove_level=False)[0]
                for model in models
            ]
        )

        schema = self._update_schema(
            schema={result["title"]: {"title": result["title"], **result}},
            models=models,
        )
        self.add_schema_definitions(schema)
        ref = {"$ref": f"#/components/schemas/{result['title']}"}

        return ref, content_type

    def _add_manually_added_schemas_to_schema(self):
        for model_or_enum in MANUALLY_ADDED_SCHEMAS:
            if issubclass(model_or_enum, Enum | TextChoices | IntegerChoices):
                m_schema = enum_process_schema(model_or_enum)
            else:
                m_schema = HumpsUtil.camelize(
                    self._create_schema_from_model(model_or_enum, remove_level=False)[0]
                )
            schema = {m_schema["title"]: HumpsUtil.camelize(m_schema)}
            self.schemas.update(schema)

    def get_components(self):
        self._add_manually_added_schemas_to_schema()
        return super().get_components()
