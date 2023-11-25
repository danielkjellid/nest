from __future__ import annotations

from typing import Any, TypeVar

from django.conf import settings
from pydantic.schema import schema as pydantic_schema

from nest.core.openapi import EnumDict, NestOpenAPISchema

from .models import Form

F = TypeVar("F", bound=Form)

COMPONENTS = settings.FORM_COMPONENT_MAPPING_DEFAULTS


class NestForms(NestOpenAPISchema):
    def __init__(self) -> None:
        super().__init__(is_form=True)
        self.app_forms: dict[str, AppForms] = {}
        self.enum_mappings: dict[str, dict[str, list[EnumDict]]] = {}
        self.meta_mappings: dict[str, dict[str, str | int]] = {}

    def add_forms(self, app_form: AppForms) -> None:
        self.app_forms[app_form.app] = app_form

    def generate_schema(self) -> dict[str, Any]:
        """
        Generate a schema in OpenAPI format for all registered forms.
        """

        forms_to_generate = []

        for app_form in self.app_forms.values():
            for form in app_form.forms:
                self.meta_mappings.update(
                    {form.__name__: {"columns": getattr(form, "COLUMNS", 1)}}
                )
                self.enum_mappings.update(self.extract_enum_from_model(form))
            forms_to_generate.extend(app_form.forms)

        schema = pydantic_schema(forms_to_generate)
        schema["definitions"] = self.modify_component_definitions(
            definitions=schema["definitions"],
            enum_mapping=self.enum_mappings,
            meta_mapping=self.meta_mappings,
            form_mapping=[],
        )

        return schema


class AppForms:
    def __init__(self, app: str) -> None:
        self.app = app
        self.forms: list[Any] = []

    def register_form(self, form: Any) -> None:
        self.forms.append(form)
