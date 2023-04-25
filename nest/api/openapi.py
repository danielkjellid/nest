from ninja.openapi.schema import (
    OpenAPISchema,
    BODY_CONTENT_TYPES,
    merge_schemas,
    resolve_allOf,
)
from pydantic.schema import model_type_schema
from django.conf import settings
from ninja import NinjaAPI
from typing import Any, get_type_hints, get_args
from enum import Enum
from django.db.models import TextChoices, IntegerChoices


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

    def _populate_request_body_form_properties(self):
        ...

    def _create_multipart_schema_from_models(self, models) -> tuple[Any, str]:
        # We have File and Form or Body, so we need to use multipart (File)
        content_type = BODY_CONTENT_TYPES["file"]

        # get the various schemas
        result = merge_schemas(
            [
                self._create_schema_from_model(model, remove_level=False)[0]
                for model in models
            ]
        )

        enum_mapping = self._extract_enum_from_models(models=models)
        result_properties = result["properties"]

        for property, property_value in result_properties.copy().items():
            property_type = property_value.get("type", None)
            for key, value in property_value.copy().items():
                if key == "component" and property_type:
                    result_properties[property][
                        key
                    ] = settings.FORM_COMPONENT_MAPPING_DEFAULTS[
                        property_value["type"]
                    ].value

                for mapping in enum_mapping:
                    if mapping["field"] == property:
                        result_properties[property]["enum"] = mapping["enum"]

        result["title"] = "MultiPartBodyParams"
        result["properties"] = result_properties

        return result, content_type
