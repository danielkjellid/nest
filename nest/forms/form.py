from enum import Enum
from typing import Any, Type

import structlog
from django.conf import settings
from django.db.models import IntegerChoices, TextChoices
from ninja import Schema

from nest.core.utils.humps import HumpsUtil

from .helpers import get_inner_list_type, is_list, is_pydantic_model
from .records import (
    FormElementEnumRecord,
    FormElementRecord,
    FormRecord,
)
from .types import JSONSchema, JSONSchemaProperties

logger = structlog.getLogger()


class Form:
    class SkipParentFormElementCreationException(Exception):
        ...

    @classmethod
    def create_from_schema(
        cls,
        *,
        schema: Schema,
        is_multipart_form: bool = False,
    ) -> FormRecord[None] | None:
        """
        Create a JSON form based on a defined schema.
        """

        schema_type, schema_is_list = cls._validate_schema(schema=schema)

        if schema_type is None:
            return None

        schema_definition = schema.schema()

        elements = cls._build_form_elements(
            schema=schema,
            schema_properties=schema_definition["properties"],
            schema_definitions=schema_definition.get("definitions", None),
            parent=None,
        )
        schema_required = schema_definition.get("required", [])
        required = [HumpsUtil.camelize(key) for key in schema_required]
        blocks_with_defaults = [
            element.id for element in elements if element.default_value is not None
        ]

        # Only exclude fields with default as None from the required list, and not all
        # fields with set defaults.
        required = required + blocks_with_defaults  # type: ignore

        return FormRecord[schema](  # type: ignore
            key=schema_definition["title"],
            is_multipart_form=is_multipart_form,
            expects_list=schema_is_list,
            required=required,  # type: ignore
            elements=elements,
        )

    @classmethod
    def _build_form_elements(  # noqa
        cls,
        schema: Schema,
        schema_properties: JSONSchemaProperties,
        schema_definitions: dict[str, JSONSchema | JSONSchemaProperties] | None,
        parent: str | None = None,
    ) -> list[FormElementRecord]:
        """
        Build form elements based on provided schema properties.
        """

        form_elements = []
        definitions = schema_definitions if schema_definitions else {}

        for key, value in schema_properties.items():
            camelized_key: str = HumpsUtil.camelize(key)  # type: ignore
            property_values: JSONSchemaProperties = cls._extract_property_values(value)
            property_all_of_list = value.get("allOf", [])  # type: ignore
            property_value_ref = value.get("$ref", None)  # type: ignore

            if parent:
                property_values["parent"] = parent

            # If we find any reference values we want to add them to a list to later
            # iterate over them and add their definitions as form blocks.
            if property_value_ref:
                property_all_of_list.append(value)

            if property_all_of_list and definitions:
                try:
                    for reference in property_all_of_list:
                        # Get the typename from the reference and find it in the
                        # definitions' dict.
                        definition_key = reference.get("$ref", "").rsplit("/", 1)[-1]
                        definition = definitions.get(definition_key, None)

                        if not definition:
                            break

                        # Replace values with values in the definition.
                        property_values["title"] = key.title().replace("_", " ")
                        property_values["type"] = definition.get("type", None)
                        definition_enum = definition.get("enum", None)
                        definition_properties = definition.get("properties", None)

                        if definition_enum:
                            field_type = schema.__fields__[key].type_
                            property_values["type"] = "enum"
                            property_values["enum"] = cls._format_enum_from_type(
                                typ=field_type
                            )

                        # If the schema references another schema, that definition will
                        # have a dict of its own properties. We want to flatten the
                        # form, and add these values, and remove the reference property.
                        if definition_properties:
                            properties_form_blocks = cls._build_form_elements(
                                schema=schema,
                                schema_properties=definition_properties,  # type: ignore
                                schema_definitions=None,
                                parent=key,
                            )
                            form_elements.extend(properties_form_blocks)
                            # Do not include reference object, so continue to the next
                            # iteration.
                            raise cls.SkipParentFormElementCreationException
                except cls.SkipParentFormElementCreationException:
                    continue

            property_value_type = property_values.get("type", None)
            if (
                not property_values.get("element", None)
                and property_value_type
                and isinstance(property_value_type, str)
            ):
                property_values["element"] = settings.FORM_ELEMENT_MAPPING_DEFAULTS[
                    property_value_type
                ]

            # The record returned does not support all keys in the JSONSchemaProperties
            # dict, therefore, we just remove the ones we don't care about before
            # initializing the record.
            all_property_values_keys: list[str] = list(property_values.keys())
            all_form_element_record_fields: list[str] = list(
                FormElementRecord.__fields__.keys()
            )
            property_values_keys_to_remove = set(all_property_values_keys) - set(
                all_form_element_record_fields
            )
            for key_to_remove in property_values_keys_to_remove:
                property_values.pop(key_to_remove)  # type: ignore

            # Append element created to the elements array.
            form_elements.append(FormElementRecord(id=camelized_key, **property_values))  # type: ignore

        return form_elements

    @staticmethod
    def _validate_schema(schema: Schema) -> tuple[Type[Schema] | None, bool]:
        """
        Validate that passed schema is either a subclassed pydantic model, or a list of
        subclassed pydantic models.
        """
        if is_list(obj=schema):
            inner_type, is_lst = get_inner_list_type(obj=schema)

            if is_pydantic_model(obj=inner_type):
                schema_from_type = inner_type
                return schema_from_type, is_lst
        elif is_pydantic_model(obj=schema):
            schema_from_type = type(schema)
            return schema_from_type, False

        else:
            logger.info(
                "Could not generate form from passed schema. Schema is not a pydantic "
                "subclass nor a list of pydantic subclasses.",
                schema=schema,
                is_list=False,
            )
        return None, is_list(obj=schema)

    @staticmethod
    def _format_enum_from_type(typ: Any) -> list[FormElementEnumRecord]:
        """
        Format schema field's enum type into a key - value format, taking advantage
        of Django's human-readable labels where applicable.
        """

        # If passed enum is a django choices field, we can take advantaged
        # of the defined label.
        if issubclass(typ, IntegerChoices | TextChoices):
            formatted_label_values = [
                FormElementEnumRecord(name=item.label, value=item.value) for item in typ
            ]
        elif issubclass(typ, Enum):
            formatted_label_values = [
                FormElementEnumRecord(
                    name=item.name.replace("_", " ").title(), value=item.value
                )
                for item in typ
            ]
        else:
            formatted_label_values = [
                FormElementEnumRecord(name=item, value=item) for item in typ
            ]

        return formatted_label_values

    @staticmethod
    def _extract_property_values(value: Any) -> JSONSchemaProperties:
        property_keys_schema_mapping = {
            "default_value": "default",
            "enum": "enum",
            "all_of": "allOf",
            "exclusive_maximum": "exclusiveMaximum",
            "exclusive_minimum": "exclusiveMinimum",
            "multiple_of": "multipleOf",
            "min_items": "minItems",
            "max_items": "maxItems",
            "unique_items": "uniqueItems",
            "min_length": "minLength",
            "max_length": "maxLength",
        }
        # If no mapping is provided, we'll fall back to use the key in supported keys.
        supported_property_keys = list(FormElementRecord.__fields__.keys())
        property_values: JSONSchemaProperties = {}

        for key in supported_property_keys:
            mapped_key = property_keys_schema_mapping.get(key, None)
            key_to_get = mapped_key if mapped_key else key
            value_to_append = value.get(key_to_get, None)

            if value_to_append is None:
                continue

            property_values[key] = value_to_append  # type: ignore
        return property_values
