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
from collections import defaultdict
from inspect import isclass
from django.db.models import IntegerChoices, TextChoices
from enum import Enum
from nest.api.files import UploadedFile, UploadedImageFile
from pydantic import BaseModel
import structlog
from django.conf import settings
from store_kit.utils import camelize
from .types import (
    Property,
    DefinitionEnum,
    Definition,
    PropertyBase,
    PropertyExtra,
    EnumDict,
)

logger = structlog.get_logger()

TModel = TypeVar("TModel", bound=BaseModel)
TEnum = TypeVar("TEnum", bound=Enum)


class NestOpenAPISchema:
    def modify_component_definitions(
        self,
        definitions: dict[str, Definition],
        meta_mapping: dict[str, str],
        enum_mapping: dict[str, EnumDict],
        is_form: bool = False,
    ) -> dict[str, Definition]:
        modified_definitions = defaultdict(dict)

        for key, attributes in definitions.items():
            modified_definition = defaultdict(dict)

            required = attributes.get("required", None)
            properties = attributes.get("properties", None)
            type_ = attributes.get("type", None)
            description = attributes.get("description", None)
            enum = attributes.get("enum", None)

            title_for_definition = meta_mapping.get(key, {}).get("title", None)
            columns_for_definition = meta_mapping.get(key, {}).get("columns", None)

            if title_for_definition is not None:
                modified_definition["title"] = title_for_definition
            else:
                modified_definition["title"] = key

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
                    is_form=is_form,
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
        is_form: bool = False,
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

            base_defaults = {
                "title": title,
                "type": type_,
            }
            extra_defaults = {
                # "help_text": val.get("help_text", None),
                "default_value": val.get("default_value", None),
                "placeholder": val.get("placeholder", None),
                "hidden_label": val.get("hidden_label", None),
                "col_span": val.get("col_span", None),
                "section": val.get("section", None),
                "order": val.get("order", None),
                "min": val.get("min", None),
                "max": val.get("max", None),
            }

            default = val.get("default", None)

            if default is not None:
                extra_defaults["default"] = default

            if not is_form:
                if enum_mapping_exists:
                    modified_property = PropertyBase(
                        **base_defaults, enum=enum_mapping[definition_key][key]
                    )
                else:
                    modified_property = PropertyBase(**base_defaults)
            else:
                if enum_mapping_exists:
                    modified_property = PropertyExtra(
                        title=title,
                        help_text=val.get("help_text", None),
                        component=settings.FORM_COMPONENT_MAPPING_DEFAULTS[
                            "enum"
                        ].value,
                        enum=enum_mapping[definition_key][key],
                        **extra_defaults,
                        type="string",  # TODO: switch places here
                    )
                else:
                    modified_property = PropertyExtra(
                        title=title,
                        help_text=val.get("help_text", None),
                        component=self.get_component(val),
                        # **base_defaults, # TODO comment in
                        **extra_defaults,
                        type=type_,
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

    def extract_meta_from_model(
        self, model: TModel, is_form: bool = False
    ) -> dict[str, str]:
        key = model.__name__
        meta_mapping = defaultdict(dict)

        for field_name, type_annotation in get_type_hints(model).items():
            if isclass(type_annotation) and issubclass(type_annotation, BaseModel):
                return self.extract_meta_from_model()

        meta_mapping["title"] = key

        if is_form:
            columns = getattr(model, "COLUMNS", None)
            if columns is None:
                meta_mapping[key]["columns"] = 1
                logger.info(
                    "Column property for model does not exist, setting columns to 1",
                    model=model,
                )
            else:
                meta_mapping[key]["columns"] = columns

        return dict(meta_mapping)

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

    @staticmethod
    def process_enum_schema(enum: Type[TEnum]) -> DefinitionEnum:
        """
        Process enum and create a dict of openapi spec.
        """
        import inspect

        # TODO: instanciate typeddict
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
