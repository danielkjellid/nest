from __future__ import annotations
from typing import TypeVar, Any
from .form import Form
from pydantic.schema import schema as pydantic_schema
from store_kit.utils import camelize
from django.conf import settings

F = TypeVar("F", bound=Form)


class NestForms:
    app_forms: dict[str, AppForms] = {}

    def add_forms(self, app_form: AppForms):
        self.app_forms[app_form.app] = app_form

    def generate_schema(self):
        columns = {}
        forms_to_generate = []

        for app, app_form in self.app_forms.items():
            for form in app_form.forms:
                columns[form.__name__] = form.COLUMNS

            forms_to_generate.extend(app_form.forms)

        schema = pydantic_schema(forms_to_generate)
        schema_definitions = schema["definitions"]

        for key, attributes in schema_definitions.items():
            schema_definitions[key]["columns"] = columns[key]
            properties = attributes["properties"]

            for property_key, property_val in properties.items():
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

        return settings.FORM_COMPONENT_MAPPING_DEFAULTS[property_val["type"]].value


class AppForms:
    def __init__(self, app: str) -> None:
        self.app = app
        self.forms: list[F] = []

    def register_form(self, form: F):
        self.forms.append(form)
