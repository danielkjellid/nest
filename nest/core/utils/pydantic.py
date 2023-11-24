from typing import Any, Iterator, Sequence, Type, TypeVar

from ninja import Schema
from pydantic import BaseModel, create_model
from pydantic.fields import ModelField

from nest.forms.fields import FormField

M = TypeVar("M", bound=Type[BaseModel])

__all__ = ["Partial", "Exclude"]


class PartialFactory:
    def __init__(self) -> None:
        ...

    def partial(
        self,
        model: M,
        fields: Sequence[str],
        overrides: dict[str, tuple[Type, FormField]] | None = None,
    ):
        return self.create_schema(
            name=model.__name__,
            model=model,
            fields=fields,
            overrides=overrides,
        )

    def exclude(
        self,
        model: M,
        fields: Sequence[str],
        overrides: dict[str, tuple[Type, FormField]] | None = None,
    ):
        return self.create_schema(
            name=model.__name__,
            model=model,
            exclude=fields,
            overrides=overrides,
        )

    def create_schema(
        self,
        name: str,
        model: M,
        fields: Sequence[str] | None = None,
        exclude: Sequence[str] | None = None,
        *,
        overrides: dict[str, tuple[Type, FormField]] | None = None,
        base_class: Type[Schema] = Schema,
    ):
        """
        Create a partial version of a pydantic model. Useful when only the partial data
        is needed.
        """

        definitions: dict[str, tuple[Type, Any | FormField]] = {}
        fields_to_exclude = set(exclude or []) - set(
            overrides.keys() if overrides else []
        )

        for field in self._selected_pydantic_model_fields(
            model=model, fields=fields, exclude=fields_to_exclude
        ):
            field_name = field.name
            field__type = field.outer_type_
            field_info = field.field_info

            definitions[field_name] = (field__type, field_info)

        if overrides:
            for field_name, field_value in overrides.items():
                outer_type, field_info = field_value
                definitions[field_name] = (outer_type, field_info)

        schema: Type[Schema] = create_model(
            name,
            __config__=None,
            __base__=base_class,
            __module__=base_class.__module__,
            __validators__={},
            **definitions,
        )

        return schema

    @staticmethod
    def _selected_pydantic_model_fields(
        model: M,
        fields: Sequence[str] | None = None,
        exclude: Sequence[str] | None = None,
    ) -> Iterator[ModelField]:
        model_fields = model.__fields__

        all_fields: dict[str, ModelField] = model_fields
        fields_to_iter = fields if fields else all_fields
        excluded_fields = set(exclude or [])
        invalid_fields = (set(fields or []) | excluded_fields) - model_fields.keys()

        if invalid_fields:
            raise ValueError(
                f"Field(s) {invalid_fields} are not in pydantic model {model}"
            )

        for field_name in model_fields.keys():
            if field_name not in fields_to_iter or field_name in set(exclude or []):
                continue

            yield all_fields[field_name]


factory = PartialFactory()

Partial = factory.partial
Exclude = factory.exclude
