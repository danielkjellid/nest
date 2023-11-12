from __future__ import annotations
from typing import TypeVar
from .form import Form
from pydantic.schema import schema as pydantic_schema
import json

F = TypeVar("F", bound=Form)


class NestForms:
    app_forms: dict[str, AppForms] = {}

    def add_forms(self, app_form: AppForms):
        self.app_forms[app_form.app] = app_form

    def generate_schema(self):
        forms_to_generate = []

        for app, app_form in self.app_forms.items():
            print(app_form.forms)
            forms_to_generate.extend(app_form.forms)

        schema = pydantic_schema(forms_to_generate)

        # Extract definitions to flat map the forms json.
        schema = schema["definitions"]

        return schema


class AppForms:
    def __init__(self, app: str) -> None:
        self.app = app
        self.forms: list[F] = []

    def register_form(self, form: F):
        self.forms.append(form)
