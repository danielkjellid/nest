from __future__ import annotations
from typing import TypeVar, Any, get_type_hints, get_args
from .form import Form
import inspect
from enum import Enum
from django.db.models import TextChoices, IntegerChoices
from pydantic.schema import schema as pydantic_schema
from store_kit.utils import camelize
from django.conf import settings

F = TypeVar("F", bound=Form)

COMPONENTS = settings.FORM_COMPONENT_MAPPING_DEFAULTS


class NestForms:
    app_forms: dict[str, AppForms] = {}
    enum_mappings = {}

    def add_forms(self, app_form: AppForms):
        self.app_forms[app_form.app] = app_form

    def generate_schema(self):
        columns = {}
        forms_to_generate = []

        for app, app_form in self.app_forms.items():
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

            for property_key, property_val in properties.items():
                # Handle property explicitly if the value is supposed to be an enum.
                if property_key in self.enum_mappings.keys():
                    mapping = self.enum_mappings[property_key]
                    property_val["title"] = property_key.title()
                    property_val["enum"] = mapping
                    property_val["type"] = "string"
                    property_val["component"] = COMPONENTS["enum"].value
                    property_val["x-enum-varnames"] = [map["label"] for map in mapping]

                    del property_val["allOf"]
                else:
                    properties[property_key]["component"] = self._get_component(
                        property_val
                    )

            schema_definitions[key]["properties"] = camelize(properties)

        return schema

    @staticmethod
    def _get_component(property_val: dict[str, Any]):
        defined_component = property_val.get("component", None)

        if defined_component is not None:
            return defined_component

        return COMPONENTS[property_val["type"]].value

    def _extract_enum_from_form(self, form: F):
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
        self.forms: list[F] = []

    def register_form(self, form: F):
        self.forms.append(form)
