from ninja.openapi.schema import (
    OpenAPISchema,
    BODY_CONTENT_TYPES,
    merge_schemas,
)
from pydantic.schema import enum_process_schema
from django.conf import settings
from ninja import NinjaAPI
from typing import Any, get_type_hints, get_args
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
        typ_union = get_args(typ)

        if typ_union:
            type_to_check = next(
                (item for item in typ_union if issubclass(item, Enum)), None
            )

            if not type_to_check:
                raise ValueError("Not able to determine enum class in tuple.")

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
        props = properties.copy()

        for property, property_value in props.items():
            property_type = property_value.get("type", None)
            for _key, _value in property_value.copy().items():
                for mapping in enum_mapping:
                    if mapping["field"] == property:
                        props[property]["enum"] = mapping["enum"]
                        props[property][
                            "component"
                        ] = settings.FORM_COMPONENT_MAPPING_DEFAULTS["enum"].value

                if property_type and props[property].get("component", None) is None:
                    props[property][
                        "component"
                    ] = settings.FORM_COMPONENT_MAPPING_DEFAULTS[
                        property_value["type"]
                    ].value
        return {"properties": HumpsUtil.camelize(props)}

    @staticmethod
    def _set_form_title_meta(models) -> dict[str, any]:
        title_meta = {}

        for model in models:
            for key, value in get_type_hints(model).items():
                if issubclass(value, UploadedFile | UploadedImageFile):
                    continue

                title_meta["title"] = f"{value.__name__}"

                if hasattr(value, "FormMeta"):
                    title_meta["columns"] = getattr(value.FormMeta, "columns", 1)

        if not title_meta["title"]:
            raise ValueError("Not able to decode form title from provided models.")

        return title_meta

    def _create_multipart_schema_from_models(self, models) -> tuple[Any, str]:
        # We have File and Form or Body, so we need to use multipart (File)
        schema = {}
        content_type = BODY_CONTENT_TYPES["file"]
        enum_mapping = self._extract_enum_from_models(models=models)

        result = merge_schemas(
            [
                self._create_schema_from_model(model, remove_level=False)[0]
                for model in models
            ]
        )

        schema.update(self._set_form_title_meta(models=models))
        schema.update(
            self._populate_request_body_form_properties(
                properties=result["properties"], enum_mapping=enum_mapping
            )
        )
        schema.update(type="object", required=result["required"])
        self.schemas.update({schema["title"]: schema})

        return {"$ref": f"#/components/schemas/{schema['title']}"}, content_type

    def _add_manually_added_schemas_to_schema(self):
        for model_or_enum in MANUALLY_ADDED_SCHEMAS:
            if issubclass(model_or_enum, Enum | TextChoices | IntegerChoices):
                m_schema = enum_process_schema(model_or_enum)
            else:
                m_schema = self._create_schema_from_model(
                    model_or_enum, remove_level=False
                )[0]
            schema = {m_schema["title"]: HumpsUtil.camelize(m_schema)}
            self.schemas.update(schema)

    def get_components(self):
        self._add_manually_added_schemas_to_schema()
        return super().get_components()
