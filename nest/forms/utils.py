from ninja import Schema
from typing import Any, TypeVar, Final
from .types import JSONSchemaProperties, JSONSchema
from .helpers import is_list, is_pydantic_model, get_inner_list_type
from .records import (
    FormRecord,
    FormSectionRecord,
    FormElementRecord,
    FormElementEnumRecord,
)
from nest.core.utils.humps import HumpsUtil
from django.db.models import TextChoices, IntegerChoices
from enum import Enum
import structlog
from django.conf import settings

logger = structlog.getLogger()

T_JSON_SCHEMA_PROPERTIES = TypeVar(
    "T_JSON_SCHEMA_PROPERTIES", bound=dict[str, str | JSONSchemaProperties]
)
T_JSON_SCHEMA_DEFINITIONS = TypeVar(
    "T_JSON_SCHEMA_DEFINITIONS", bound=dict[str, JSONSchema | JSONSchemaProperties]
)


class FormUtil:
    class SkipParentFormElementCreationException(Exception):
        ...

    @classmethod
    def create_form_from_schema(
        cls,
        *,
        schema: Schema,
        is_multipart_form: bool = False,
        sections: list[FormSectionRecord] | None = None,
    ) -> FormRecord | None:
        """
        Create a JSON form based on a defined schema.
        """

        sections = sections if sections is not None else []
        schema_type, schema_is_list = cls._validate_schema(schema=schema)

        if schema_type is None:
            return

        schema_definition = schema_type.schema()

        elements = cls._build_form_elements(
            cls,
            schema_type_annotation=schema_type,
            schema_properties=schema_definition["properties"],
            schema_definitions=schema_definition.get("definitions", None),
            parent=None,
        )
        schema_required = schema_definition.get("required", [])
        required = [HumpsUtil.camelize(key) for key in schema_required]
        blocks_with_defaults = [
            element.id for element in elements if element.default is not None
        ]

        # Only exclude fields with default as None from the required list, and not all
        # fields with set defaults.
        required = required + blocks_with_defaults

        return FormRecord(
            key=schema_definition["title"],
            is_multipart_form=is_multipart_form,
            expects_list=schema_is_list,
            required=required,
            sections=sections,
            elements=elements,
        )

    def _build_form_elements(
        self,
        schema_type_annotation: Schema,
        schema_properties: T_JSON_SCHEMA_PROPERTIES,
        schema_definitions: T_JSON_SCHEMA_DEFINITIONS | None,
        parent: str | None = None,
    ) -> list[FormElementRecord]:
        """
        Build form elements based on provided schema properties.
        """

        form_elements = []
        definitions = schema_definitions if schema_definitions else {}

        for key, value in schema_properties.items():
            camelized_key = HumpsUtil.camelize(key)
            property_values = self._extract_property_values(value)
            property_all_of_list = value.get("allOf", [])
            property_value_ref = value.get("$ref", None)

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
                        property_values["title"] = camelized_key.title()
                        property_values["type"] = definition.get("type", None)
                        definition_enum = definition.get("enum", None)
                        definition_properties = definition.get("properties", None)

                        if definition_enum:
                            field_type = schema_type_annotation.__fields__[key].type_
                            property_values["type"] = "enum"
                            property_values["enum"] = self._format_enum_from_type(
                                typ=field_type
                            )

                        # If the schema references another schema, that definition will
                        # have a dict of its own properties. We want to flatten the
                        # form, and add these values, and remove the reference property.
                        if definition_properties:
                            properties_form_blocks = self._build_form_elements(
                                schema_type_annotation=schema_type_annotation,
                                schema_properties=definition_properties,
                                schema_definitions=None,
                                parent=camelized_key,
                            )
                            form_elements.extend(properties_form_blocks)
                            # Do not include reference object, so continue to the next
                            # iteration.
                            raise self.SkipParentFormElementCreationException
                except self.SkipParentFormElementCreationException:
                    continue

            if not property_values.get("element", None):
                property_values["element"] = settings.FORM_ELEMENT_MAPPING_DEFAULTS[
                    property_values["type"]
                ]

            form_elements.append(FormElementRecord(id=camelized_key, **property_values))

        return form_elements

    @staticmethod
    def _validate_schema(schema: Schema) -> tuple[type | None, bool]:
        """
        Validate that passed schema is either a subclassed pydantic model, or a list of
        subclassed pydantic models.
        """
        if is_list(type_annotation=schema):
            inner_type, is_lst = get_inner_list_type(type_annotation=schema)

            if is_pydantic_model(type_annotation=inner_type):
                schema_from_type = inner_type
                return schema_from_type, is_lst

        elif is_pydantic_model(type_annotation=schema):
            schema_from_type = schema
            return schema_from_type, False

        else:
            logger.info(
                "Could not generate form from passed schema. Schema is not a pydantic "
                "subclass nor a list of pydantic subclasses.",
                schema=schema,
                is_list=False,
            )
            return None, is_list(schema)

    @staticmethod
    def _format_enum_from_type(typ: type) -> list[FormElementEnumRecord]:
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
    def _extract_property_values(value: Any) -> dict[str, Any]:
        property_keys_schema_mapping = {
            "default": "default",
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
        supported_property_keys = [key for key in FormElementRecord.__fields__.keys()]
        property_values = {}

        for key in supported_property_keys:
            mapped_key = property_keys_schema_mapping.get(key, None)
            key_to_get = mapped_key if mapped_key else key
            value_to_append = value.get(key_to_get, None)

            if value_to_append is None:
                continue

            property_values[key] = value_to_append
        return property_values
