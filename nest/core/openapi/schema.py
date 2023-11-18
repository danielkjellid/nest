from collections import defaultdict
from copy import deepcopy
from enum import Enum
from inspect import isclass
from typing import (
    Any,
    Iterable,
    Type,
    TypeVar,
    cast,
    get_args,
    get_type_hints,
)

import structlog
from django.conf import settings
from django.db.models import IntegerChoices, TextChoices
from pydantic import BaseModel
from store_kit.utils import camelize

from .types import (
    Definition,
    DefinitionEnum,
    EnumDict,
    Property,
    PropertyBase,
    PropertyExtra,
)

logger = structlog.get_logger()

TModel = TypeVar("TModel", bound=BaseModel)
TEnum = TypeVar("TEnum", bound=Enum)


class NestOpenAPISchema:
    def __init__(self, is_form: bool = False) -> None:
        self.is_form = is_form

    def modify_component_definitions(
        self,
        definitions: dict[str, Definition],
        meta_mapping: dict[str, str],
        enum_mapping: dict[str, EnumDict],
    ) -> dict[str, Definition]:
        modified_definitions = defaultdict(dict)

        for key, attributes in deepcopy(definitions).items():
            modified_definition = defaultdict(dict)

            required = attributes.get("required", None)
            properties = attributes.get("properties", None)
            type_ = attributes.get("type", None)
            description = attributes.get("description", None)
            enum = attributes.get("enum", None)

            columns_for_definition = meta_mapping.get(key, {}).get("columns", None)

            modified_definition["title"] = attributes.get("title", key)

            if description is not None:
                modified_definition["description"] = description

            if enum is not None:
                modified_definition["enum"] = enum

            if type_:
                modified_definition["type"] = type_

            if properties is not None:
                modified_properties = self.modify_component_definitions_properties(
                    definition_key=key,
                    properties=properties,
                    enum_mapping=enum_mapping,
                )
                modified_definition["properties"] = modified_properties

            if required is not None:
                modified_definition["required"] = self.convert_keys_to_camelcase(
                    required
                )

            if columns_for_definition is not None:
                modified_definition["columns"] = columns_for_definition

            modified_definitions[key] = modified_definition

        return dict(modified_definitions)

    def modify_component_definitions_properties(
        self,
        *,
        definition_key: str,
        properties: dict[str, Property],
        enum_mapping: dict[str, list[EnumDict]],
    ) -> dict[str, Property]:
        modified_properties: dict[str, Property] = defaultdict(dict)

        for key, val in properties.items():
            enum_mapping_exists = (
                definition_key in enum_mapping.keys()
                and key in enum_mapping[definition_key].keys()
            )

            title = key.replace("_", " ").title()
            type_ = val.get("type", None)

            val.pop("allOf", None)
            val.pop("anyOf", None)
            val_copy = val.copy()
            val.pop("component", None)

            base_defaults = {}

            if "$ref" not in val:
                base_defaults["title"] = title

            if type_ is not None:
                base_defaults["type"] = type_

            extra_defaults = {
                "help_text": val.get("help_text", None),
                "default_value": val.get("default_value", None),
                "placeholder": val.get("placeholder", None),
                "hidden_label": val.get("hidden_label", None),
                "col_span": val.get("col_span", None),
                "section": val.get("section", None),
                "order": val.get("order", None),
                "min": val.get("min", None),
                "max": val.get("max", None),
            }

            for default_key in {**base_defaults, **extra_defaults}.keys():
                val.pop(default_key, None)

            if enum_mapping_exists:
                val.pop("enum", None)

            if not self.is_form and enum_mapping_exists:
                modified_property = PropertyBase(
                    **base_defaults,
                    **val,
                    enum=enum_mapping[definition_key][key],
                )
            elif not self.is_form and not enum_mapping_exists:
                modified_property = PropertyBase(
                    **base_defaults,
                    **val,
                )
            elif self.is_form and enum_mapping_exists:
                modified_property = PropertyExtra(
                    title=title,
                    type="string",
                    enum=enum_mapping[definition_key][key],
                    component=settings.FORM_COMPONENT_MAPPING_DEFAULTS["enum"].value,
                    **extra_defaults,
                    **val,
                )
            else:
                modified_property = PropertyExtra(
                    **base_defaults,
                    **extra_defaults,
                    component=self.get_component(val_copy),
                    **val,
                )

            modified_properties[key] = modified_property

        return self.convert_keys_to_camelcase(dict(modified_properties))

    def convert_keys_to_camelcase(self, data):
        """
        Recursively go through a dataset and convert it to camelcase.
        """
        if isinstance(data, dict):
            return {
                camelize(key): self.convert_keys_to_camelcase(val)
                for key, val in data.items()
            }
        elif isinstance(data, list):
            return [camelize(val) for val in data]
        else:
            return data

    @staticmethod
    def get_component(property_: Property) -> str:
        defined_component = property_.get("component", None)

        if defined_component is not None:
            return defined_component

        return settings.FORM_COMPONENT_MAPPING_DEFAULTS[property_["type"]].value

    def extract_enum_from_model(self, model: TModel) -> dict[str, list[EnumDict]]:
        enum_mapping = defaultdict(dict)

        # Iterate through model fields and their type annotation.
        for field_name, type_annotation in get_type_hints(model).items():
            # If we encounter a field referencing another pydantic model, recursively
            # go through the hierarchy to extract the bottom-most value.
            if isclass(type_annotation) and issubclass(type_annotation, BaseModel):
                return self.extract_enum_from_model(type_annotation)
            else:
                enum = self.format_enum_from_type(type_annotation)

                if not enum:
                    continue

                enum_mapping[model.__name__][field_name] = enum

        return dict(enum_mapping)

    def extract_enum_from_models(
        self, models: list[TModel]
    ) -> dict[str, list[EnumDict]]:
        enum_mapping = defaultdict(dict)

        for model in models:
            mapping = self.extract_enum_from_model(model)
            enum_mapping = {**enum_mapping, **mapping}

        return dict(enum_mapping)

    @staticmethod
    def process_enum_schema(enum: Type[TEnum]) -> DefinitionEnum:
        """
        Process enum and create a dict of openapi spec.
        """
        import inspect

        definition = DefinitionEnum(
            title=enum.__name__,
            # Python assigns all enums a default docstring value of 'An enumeration', so
            # all enums will have a description field even if not explicitly provided.
            description=inspect.cleandoc(enum.__doc__ or "An enumeration."),
            # Add enum values and the enum field type to the schema.
            enum=[item.value for item in cast(Iterable[Enum], enum)],
            **{
                "x-enum-varnames": [
                    getattr(item, "label", item.value)
                    for item in cast(Iterable[Enum], enum)
                ]
            },
        )

        return definition

    @staticmethod
    def format_enum_from_type(typ: Any) -> list[EnumDict] | None:
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
                    if isclass(item) and issubclass(item, Enum)
                ),
                None,
            )

            if not type_to_check:
                return None

        if not isclass(type_to_check):
            return None

        # If passed enum is a django choices field, we can take advantaged
        # of the defined label.
        if issubclass(type_to_check, IntegerChoices | TextChoices):
            return [
                EnumDict(label=item.label, value=item.value) for item in type_to_check
            ]
        elif issubclass(type_to_check, Enum):
            return [
                EnumDict(label=item.name.replace("_", " ").title(), value=item.value)
                for item in type_to_check
            ]

        return None
