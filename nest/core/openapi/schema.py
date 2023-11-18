from typing import (
    get_args,
    Any,
    TypeAlias,
    TypedDict,
    TypeVar,
    NotRequired,
    get_type_hints,
    Type,
    cast,
    Iterable,
)
from inspect import isclass
from django.db.models import IntegerChoices, TextChoices
from enum import Enum
from nest.api.files import UploadedFile, UploadedImageFile
from pydantic import BaseModel
import structlog
from django.conf import settings
from store_kit.utils import camelize
from .types import Property, DefinitionEnum, Definition, PropertyBase, PropertyExtra

logger = structlog.get_logger()
TModel = TypeVar("TModel", bound=BaseModel)
TEnum = TypeVar("TEnum", bound=Enum)


class EnumDict(TypedDict):
    label: str
    value: str | int


class NestOpenAPISchema:
    def modify_component_definition(
        self,
        definitions: dict[str, Definition],
        meta_mapping: dict[str, str],
        enum_mapping: dict[str, EnumDict],
        column_mapping: dict[str, int],
    ) -> dict[str, Definition]:
        modified_definitions = {}

        for key, attributes in definitions.items():
            modified_definition = {}

            title_for_definition = meta_mapping.get(key, {}).get("title", None)
            columns_for_definition = meta_mapping.get(key, {}).get("columns", None)

            required = attributes.get("required", None)
            properties = attributes.get("properties", None)

            if title_for_definition is not None:
                modified_definition[key]["title"] = title_for_definition
            else:
                modified_definition[key]["title"] = key

            if columns_for_definition is not None:
                modified_definition[key]["columns"] = columns_for_definition

            if required is not None:
                modified_definition[key]["required"] = self.convert_keys_to_camelcase(
                    required
                )

            if properties is not None:
                modified_properties = self.modify_component_definition_properties(
                    properties=properties, is_form=False, enum_mapping=enum_mapping
                )
                modified_definition[key]["properties"] = modified_properties

            modified_definitions[key] = modified_definition

        return modified_definitions

    def modify_component_definition_properties(
        self,
        *,
        properties: dict[str, Property],
        is_form: bool = False,
        enum_mapping: dict[str, list[EnumDict]],
    ) -> dict[str, Property]:
        modified_properties: dict[str, Property] = {}

        for key, val in properties.items():
            title = key.title()
            type_ = val.get("type", None)

            # TODO: Check if enum mapping exists, if so, add enum property

            val.pop("allOf", None)
            val.pop("anyOf", None)

            if not is_form:
                modified_property = PropertyBase(title=title, type=type_)
            else:
                modified_property = PropertyExtra(
                    title=title,
                    type=type_,
                    help_text=val.get("help_text", None),
                    component=self.get_component(val),
                    default_value=val.get("default_value", None),
                    placeholder=val.get("placeholder", None),
                    hidden_label=val.get("hidden_label", None),
                    col_span=val.get("col_span", None),
                    order=val.get("order", None),
                    min=val.get("min", None),
                    max=val.get("max", None),
                )

            modified_properties[key] = modified_property

        return modified_properties

    def convert_keys_to_camelcase(self, data):
        """
        Recursively go through a dataset and convert it to camelcase.
        """
        if isinstance(data, dict):
            return {
                key: self.convert_keys_to_camelcase(val) for key, val in data.items()
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

    @staticmethod
    def extract_meta_from_model(model: TModel, is_form: bool = False) -> dict[str, str]:
        meta_mapping = {}

        for field_name, type_annotation in get_type_hints(model).items():
            meta = {}
            class_ = next(
                (val for val in get_args(type_annotation) if isclass(val)), None
            )

            if class_ is None or issubclass(class_, (UploadedFile, UploadedImageFile)):
                continue

            if is_form:
                columns = getattr(model, "COLUMNS", None)
                if columns is None:
                    meta["columns"] = 1
                    logger.info(
                        "Column property for model does not exist, setting columns to 1",
                        model=model,
                    )
                else:
                    meta["columns"] = columns

            meta["title"] = class_.__name__

            meta_mapping[model.__name__] = meta

        return meta_mapping

    def extract_enum_from_model(self, model: TModel) -> dict[str, list[EnumDict]]:
        enum_mapping = {}

        for field_name, annotation in model.__fields__.items():
            enum = self.format_enum_from_type(annotation.type_)

            if not enum:
                continue

            enum_mapping[field_name] = enum

        return enum_mapping

    @staticmethod
    def process_enum_schema(enum: Type[TEnum]) -> DefinitionEnum:
        """
        Process enum and create a dict of openapi spec.
        """
        import inspect

        definition: DefinitionEnum = {
            "title": enum.__name__,
            # Python assigns all enums a default docstring value of 'An enumeration', so
            # all enums will have a description field even if not explicitly provided.
            "description": inspect.cleandoc(enum.__doc__ or "An enumeration."),
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
