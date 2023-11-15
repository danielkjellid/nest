from __future__ import annotations

import inspect
from enum import Enum
from typing import Any, TypeVar, get_args

from django.conf import settings
from django.db.models import IntegerChoices, TextChoices
from pydantic.schema import schema as pydantic_schema
from store_kit.utils import camelize

from .models import Form

F = TypeVar("F", bound=Form)

COMPONENTS = settings.FORM_COMPONENT_MAPPING_DEFAULTS


class NestForms:
    def __init__(self) -> None:
        self.app_forms: dict[str, AppForms] = {}
        self.enum_mappings: dict[str, list[dict[str, str | int]]] = {}

    def add_forms(self, app_form: AppForms) -> None:
        self.app_forms[app_form.app] = app_form

    def generate_schema(self) -> dict[str, Any]:
        """
        Generate a schema in OpenAPI format for all registered forms.
        """
        columns = {}
        forms_to_generate = []

        for app_form in self.app_forms.values():
            for form in app_form.forms:
                columns[form.__name__] = form.COLUMNS

                # Extract all types that represent an enumeration and add them to the
                # mapping property. This is because we want to later extract them and
                # replace allOf/anyOf values.
                self.enum_mappings.update(self._extract_enum_from_form(form))

            forms_to_generate.extend(app_form.forms)

        schema = pydantic_schema(forms_to_generate)
        schema_definitions = schema["definitions"]

        for key, attributes in schema_definitions.items():
            columns_for_key = columns.get(key, None)

            if columns_for_key is not None:
                schema_definitions[key]["columns"] = columns[key]

            properties = attributes.get("properties", None)

            if properties is None:
                continue

            required = attributes.get("required", None)

            if required is not None:
                attributes["required"] = [camelize(r) for r in required]

            for property_key, property_val in properties.items():
                # Handle property explicitly if the value is supposed to be an enum.
                if property_key in self.enum_mappings.keys():
                    mapping = self.enum_mappings[property_key]
                    property_val["title"] = property_key.title()
                    property_val["enum"] = mapping
                    property_val["type"] = "string"
                    property_val["component"] = COMPONENTS["enum"].value
                    property_val["x-enum-varnames"] = [map["label"] for map in mapping]

                    property_val.pop("allOf", None)
                    property_val.pop("anyOf", None)
                else:
                    properties[property_key]["component"] = self._get_component(
                        property_val
                    )

            schema_definitions[key]["properties"] = camelize(properties)

        return schema

    @staticmethod
    def _get_component(property_val: dict[str, Any]) -> str:
        """
        Get related component based on property type.
        """
        defined_component: str = property_val.get("component", None)

        if defined_component is not None:
            return defined_component

        return COMPONENTS[property_val["type"]].value

    def _extract_enum_from_form(self, form: F) -> dict[str, list[dict[str, str | int]]]:
        enum_mapping = {}

        for field_name, val in form.__fields__.items():
            enum = self._format_enum_from_type(typ=val.type_)

            if not enum:
                continue

            enum_mapping[field_name] = enum

        return enum_mapping

    def _format_enum_from_type(self, typ: Any) -> list[dict[str, str | int]] | None:
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


class AppForms:
    def __init__(self, app: str) -> None:
        self.app = app
        self.forms: list[Any] = []

    def register_form(self, form: Any) -> None:
        self.forms.append(form)
