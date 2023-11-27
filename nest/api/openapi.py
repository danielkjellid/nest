from __future__ import annotations

import inspect
from enum import Enum
from typing import (
    Any,
    Type,
    cast,
    get_args,
    get_type_hints,
)

from django.db.models import IntegerChoices, TextChoices
from ninja import NinjaAPI
from ninja.openapi.schema import (
    BODY_CONTENT_TYPES,
    REF_PREFIX,
    merge_schemas,
)
from ninja.openapi.schema import (
    OpenAPISchema as NinjaOpenAPISchema,
)
from ninja.params_models import TModel, TModels
from ninja.types import DictStrAny
from pydantic import BaseModel
from pydantic.schema import model_schema

from nest.api.files import UploadedFile, UploadedImageFile
from nest.core.openapi import NestOpenAPISchema

MANUALLY_ADDED_SCHEMAS = []
FORMS = []


def add_to_openapi_schema(decorated_class: Any) -> Any:
    """
    Decorator that can be used to manually add ninja.Schema, pydantic.BaseModel and
    enums to generated openapi schema.

    Usage:
    @add_to_openapi_schema
    class MySchema(Schema):
        ...
    """
    MANUALLY_ADDED_SCHEMAS.append(decorated_class)
    return decorated_class


def form(decorated_class: Any) -> Any:
    """
    Decorator that can be used to add forms to openapi schema.

    Usage:
    @form
    class MyForm(BaseModel):
        ...
    """
    FORMS.append(decorated_class)
    return decorated_class


def get_schema(api: NinjaAPI, path_prefix: str = "") -> OpenAPISchema:
    openapi = OpenAPISchema(api, path_prefix)
    return openapi


class OpenAPISchema(NinjaOpenAPISchema, NestOpenAPISchema):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get_components(self) -> DictStrAny:
        self._add_manually_added_schemas_to_schema()
        self._add_forms_to_schema()
        return super().get_components()

    def _update_schema(
        self,
        component_schemas: dict[str, dict[str, Any]],
        models: TModels[Any],
    ) -> dict[str, Any]:
        """
        This is where the magic happens. This method is responsible for updating the
        schema appropriately, combining all helper methods. It converts keys to
        camelcase, sets component and extract enum values.
        """

        enum_mapping = self.extract_enum_from_models(models)

        schemas = self.modify_component_definitions(
            definitions=component_schemas,
            enum_mapping=enum_mapping,
            form_mapping={
                f.__name__: {"columns": getattr(f, "COLUMNS", 1)} for f in FORMS
            },
        )

        return schemas

    def _create_schema_from_model(
        self, model: TModel, by_alias: bool = True, remove_level: bool = True
    ) -> tuple[dict[str, Any], bool]:
        """
        Overriden method that is responsible for converting the different ninja.Schema
        models to an openapi dict representation that we can use. We hook into the
        definitions part and modifies the schema before it's added to the list of
        schemas.
        """
        if hasattr(model, "_flatten_map"):
            schema = self._flatten_schema(model)
        else:
            schema = model_schema(
                cast(Type[BaseModel], model), ref_prefix=REF_PREFIX, by_alias=by_alias
            )

        if schema.get("definitions"):
            definitions = schema.pop("definitions")
            # Intercept schema definition and update it.
            updated_schema = self._update_schema(
                component_schemas=definitions, models=[model]
            )
            self.add_schema_definitions(updated_schema)

        if remove_level and len(schema["properties"]) == 1:
            name, details = next(iter(schema["properties"].items()))
            required = name in schema.get("required", {})
            return details, required
        else:
            return schema, True

    def _create_multipart_schema_from_models(
        self, models: TModels[Any]
    ) -> tuple[dict[str, str], str]:
        """
        Overriden method that is responsible for converting different ninja.Schema
        models + multipart form parameters defined in endpoints to an openapi dict
        representation that we can use. Core difference from _create_schema_from_model
        is that we're not handling multiple models instead of just one, so we need to
        flatten them first.
        """
        content_type = BODY_CONTENT_TYPES["file"]

        result: dict[str, dict[str, Any]] = {}

        for index, model in enumerate(models):
            title = self.get_title_from_nested_model(model)

            # If title is None it means that we're dealing with some sort of property
            # instead of a definition. Therefore, we instead merge it with the previous
            # definition and fix the title.
            if title is None:
                title = self.get_title_from_nested_model(models[index - 1])
                schema = merge_schemas(
                    [
                        self._create_schema_from_model(m, remove_level=False)[0]
                        for m in models[: index + 1]
                    ]
                )
            else:
                schema = self._create_schema_from_model(model, remove_level=False)[0]

            if title is None:
                continue

            schema["title"] = title
            result[title] = schema

        schema = self._update_schema(
            component_schemas=result,
            models=models,
        )
        self.add_schema_definitions(schema)

        schema_title = next(iter(schema.keys()))
        ref = {"$ref": f"#/components/schemas/{schema_title}"}

        return ref, content_type

    def _add_manually_added_schemas_to_schema(self) -> None:
        """
        Take all instances that's going to be manually added to the generated openapi
        spec through the @add_to_openapi_schema decorator and process them. The, once
        processed, add them to the schema.
        """
        for model_or_enum in MANUALLY_ADDED_SCHEMAS:
            # Enums has to be treated a bit differently than normal pydantic.BaseModel
            # or ninja.Schema.
            if issubclass(model_or_enum, Enum | TextChoices | IntegerChoices):
                m_schema = self.process_enum_schema(model_or_enum)

            else:
                m_schema = self._create_schema_from_model(
                    model_or_enum, remove_level=False
                )[0]

            self.schemas.update({m_schema["title"]: m_schema})

    def _add_forms_to_schema(self) -> None:
        for added_form in FORMS:
            key = added_form.__name__

            if key in self.schemas:
                continue

            m_schema = self._create_schema_from_model(added_form, remove_level=False)[0]

            schema = self._update_schema(
                component_schemas={key: m_schema},
                models=[added_form],
            )

            self.schemas.update(schema)

    @staticmethod
    def get_title_from_nested_model(model: TModel) -> str | None:
        for value in get_type_hints(model).values():
            val = value
            val_iterable = get_args(value)

            if val_iterable:
                val = next(
                    (item for item in val_iterable if inspect.isclass(item)),
                    None,
                )

            if not val:
                continue

            if issubclass(val, UploadedFile | UploadedImageFile):
                continue

            return str(val.__name__)

        return None
