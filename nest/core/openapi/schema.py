from typing import get_args, Any, TypeAlias, TypedDict, TypeVar, NotRequired
from inspect import isclass
from django.db.models import IntegerChoices, TextChoices
from enum import Enum
from pydantic import BaseModel
import structlog
from django.conf import settings
from store_kit.utils import camelize
from .types import Property

logger = structlog.get_logger()
COMPONENTS = settings.FORM_COMPONENT_MAPPING_DEFAULTS
T_Model = TypeVar("T_Model", bound=BaseModel)


class EnumDict(TypedDict):
    label: str
    value: str | int


class NestOpenAPISchema:
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

        return COMPONENTS[property_["type"]].value

    def extract_enum_from_model(self, model: T_Model) -> dict[str, list[EnumDict]]:
        enum_mapping = {}

        for field_name, annotation in model.__fields__.items():
            enum = self.format_enum_from_type(annotation.type_)

            if not enum:
                continue

            enum_mapping[field_name] = enum

        return enum_mapping

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
