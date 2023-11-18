from __future__ import annotations

import inspect
from enum import Enum
from typing import (
    Any,
    Collection,
    Iterable,
    Sequence,
    Type,
    cast,
    get_args,
    get_type_hints,
)

from django.conf import settings
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
from nest.core.openapi.schema import NestOpenAPISchema
from nest.core.openapi.types import Definition
from ninja.params_models import TModel, TModels
from ninja.types import DictStrAny
from pydantic import BaseModel
from pydantic.schema import model_schema
from store_kit.utils import camelize

from nest.api.files import UploadedFile, UploadedImageFile

MANUALLY_ADDED_SCHEMAS = []


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


def get_schema(api: NinjaAPI, path_prefix: str = "") -> OpenAPISchema:
    openapi = OpenAPISchema(api, path_prefix)
    return openapi


class OpenAPISchema(NinjaOpenAPISchema, NestOpenAPISchema):
    def get_components(self) -> DictStrAny:
        self._add_manually_added_schemas_to_schema()
        return super().get_components()

    def _update_schema(
        self, component_schemas: dict[str, Definition], models: TModels[Any]
    ) -> dict[str, Any]:
        """
        This is where the magic happens. This method is responsible for updating the
        schema appropriately, combining all helper methods. It converts keys to
        camelcase, sets component and extract enum values.
        """

        enum_mapping = self.extract_enum_from_models(models)
        meta_mapping = self.extract_meta_from_models(models)

        schemas = self.modify_component_definitions(
            definitions=component_schemas,
            meta_mapping=meta_mapping,
            enum_mapping=enum_mapping,
            is_form=False,
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

        result = {}

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
                        for m in models[:index]
                    ]
                )
            else:
                schema = self._create_schema_from_model(model, remove_level=False)[0]

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

    @staticmethod
    def _set_schema_meta(models: TModels[Any]) -> dict[str, Any]:
        """
        For multipart/form schemas the title is automatically populated to FormParams,
        however, we want to use the actual schema payload name. We also allow for
        multi-column forms, which is set through the subclass FormMeta on a
        ninja.Schema.
        """
        meta = {}

        for model in models:
            for _key, value in get_type_hints(model).items():
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

                meta["title"] = f"{val.__name__}"

                if hasattr(val, "FormMeta"):
                    meta["columns"] = getattr(
                        value.FormMeta,
                        "columns",
                        1,  # type: ignore
                    )

        return meta
