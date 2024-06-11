from collections import defaultdict
from copy import deepcopy
from enum import Enum
from inspect import cleandoc, isclass
from typing import (
    Any,
    Iterable,
    Type,
    TypedDict,
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

logger = structlog.get_logger()

TModel = TypeVar("TModel", bound=BaseModel)
TEnum = TypeVar("TEnum", bound=Enum)


class EnumDict(TypedDict):
    label: str
    value: str | int


class NestOpenAPISchema:
    def modify_component_definitions(
        self,
        definitions: dict[str, dict[str, Any]],
        enum_mapping: dict[str, dict[str, list[EnumDict]]],
        form_mapping: dict[str, dict[str, int]],
    ) -> dict[str, dict[str, Any]]:
        modified_definitions: dict[str, dict[str, Any]] = defaultdict(dict)

        for key, attributes in deepcopy(definitions).items():
            modified_definition: dict[str, Any] = defaultdict(dict)

            required = attributes.pop("required", None)
            properties = attributes.pop("properties", None)
            type_ = attributes.pop("type", None)
            description = attributes.pop("description", None)
            enum = attributes.pop("enum", None)

            is_form = key in form_mapping.keys()

            modified_definition["title"] = attributes.get("title", key)

            if description is not None:
                modified_definition["description"] = description

            if enum is not None:
                modified_definition["enum"] = enum

            if type_:
                modified_definition["type"] = type_

            if is_form:
                modified_definition["x-form"] = True
                modified_definition["x-columns"] = form_mapping[key]["columns"]

            if required is not None:
                modified_definition["required"] = self.convert_keys_to_camelcase(
                    required
                )

            if properties is not None:
                modified_properties = self.modify_component_definitions_properties(
                    definition_key=key,
                    properties=properties,
                    enum_mapping=enum_mapping,
                    is_form=is_form,
                )
                modified_definition["properties"] = modified_properties

            modified_definitions[key] = {**modified_definition, **attributes}

        return dict(modified_definitions)

    def modify_component_definitions_properties(
        self,
        *,
        definition_key: str,
        properties: dict[str, dict[str, Any]],
        enum_mapping: dict[str, dict[str, list[EnumDict]]],
        is_form: bool = False,
    ) -> dict[str, dict[str, Any]]:
        modified_properties: dict[str, dict[str, Any]] = defaultdict(dict)
        for key, val in properties.items():
            enum_mapping_exists = (
                definition_key in enum_mapping.keys()
                and key in enum_mapping[definition_key].keys()
            )

            title = key.replace("_", " ").title()
            type_ = val.get("type", None)

            old_val = val.copy()
            val.pop("component", None)

            base_defaults: dict[str, Any] = {}

            if "$ref" not in val:
                base_defaults["title"] = title

            if type_ is not None:
                base_defaults["type"] = type_

            extra_defaults: dict[str, Any] = {
                "x-helpText": val.pop("help_text", None),
                "x-defaultValue": val.pop("default_value", None),
                "x-placeholder": val.pop("placeholder", None),
                "x-hiddenLabel": val.pop("hidden_label", None),
                "x-colSpan": val.pop("col_span", None),
                "x-section": val.pop("section", None),
                "x-order": val.pop("order", None),
                "x-min": val.pop("min", None),
                "x-max": val.pop("max", None),
            }

            for default_key in {**base_defaults, **extra_defaults}.keys():
                val.pop(default_key, None)

            modified_property: dict[str, Any]

            if not is_form and enum_mapping_exists:
                mapped_enum = enum_mapping[definition_key][key]
                modified_property = {
                    **base_defaults,
                    "enum": [e["value"] for e in mapped_enum],
                    "x-enum": mapped_enum,
                    **val,
                }
            elif not is_form and not enum_mapping_exists:
                modified_property = {
                    **base_defaults,
                    **val,
                }
            elif is_form and enum_mapping_exists:
                mapped_enum = enum_mapping[definition_key][key]
                component = settings.FORM_COMPONENT_MAPPING_DEFAULTS["enum"].value

                modified_property = {
                    "title": title,
                    "type": "string",
                    "enum": [e["value"] for e in mapped_enum],
                    "x-enum": mapped_enum,
                    "x-component": component,
                    **extra_defaults,
                    **val,
                }
            else:
                modified_property = {
                    **base_defaults,
                    **extra_defaults,
                    "x-component": self.get_component(old_val),
                    **val,
                }

            modified_properties[camelize(key)] = modified_property  # type: ignore

        return dict(modified_properties)

    def convert_keys_to_camelcase(self, data: Any) -> Any:
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
    def get_component(property_: dict[str, Any]) -> str:
        defined_component: str = property_.get("component", None)

        if defined_component is not None:
            return defined_component

        property_format: str = property_.get("format", "")
        if property_format == "binary":
            return settings.FORM_COMPONENT_MAPPING_DEFAULTS["file"].value

        component: str = settings.FORM_COMPONENT_MAPPING_DEFAULTS[
            property_["type"]
        ].value

        return component

    def extract_enum_from_model(
        self, model: Type[TModel]
    ) -> dict[str, dict[str, list[EnumDict]]]:
        enum_mapping: dict[str, dict[str, list[EnumDict]]] = defaultdict(dict)

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
        self, models: list[Type[TModel]]
    ) -> dict[str, dict[str, list[EnumDict]]]:
        enum_mapping: dict[str, dict[str, list[EnumDict]]] = defaultdict(dict)

        for model in models:
            mapping = self.extract_enum_from_model(model)
            enum_mapping = {**enum_mapping, **mapping}

        return dict(enum_mapping)

    @staticmethod
    def process_enum_schema(enum: Type[TEnum]) -> dict[str, Any]:
        """
        Process enum and create a dict of openapi spec.
        """

        definition = {
            "title": enum.__name__,
            # Python assigns all enums a default docstring value of 'An enumeration', so
            # all enums will have a description field even if not explicitly provided.
            "description": cleandoc(enum.__doc__ or "An enumeration."),
            # Add enum values and the enum field type to the schema.
            "enum": [item.value for item in cast(Iterable[Enum], enum)],
            "x-enum-varnames": [
                getattr(item, "label", item.value)
                for item in cast(Iterable[Enum], enum)
            ],
        }

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
