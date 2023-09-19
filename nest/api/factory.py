from ninja import Schema

from typing import TypeVar, Sequence, Type, Any, Iterator
from pydantic import BaseModel, create_model
from pydantic.fields import ModelField

from .fields import FormField

M = TypeVar("M", bound=BaseModel)


class PartialFactory:
    def __init__(self) -> None:
        ...

    def create_schema(
        self,
        name: str,
        model: M,
        fields: Sequence[str],
        *,
        overrides: dict[str, tuple[Type, FormField]] | None = None,
        base_class: Type[Schema] = Schema,
    ):
        """
        Create a partial version of a pydantic model. Useful when only the partial data
        is needed.
        """

        definitions: dict[str, tuple[Type, Any | FormField]] = {}
        exclude = overrides.keys() if overrides else []

        for field in self._selected_pydantic_model_fields(
            model=model, fields=fields, exclude=exclude
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

    def _selected_pydantic_model_fields(
        self,
        model: M,
        fields: Sequence[str],
        exclude: Sequence[str] | None = None,
    ) -> Iterator[ModelField]:
        model_fields = model.__fields__

        all_fields: dict[str, ModelField] = model_fields
        invalid_fields = (set(fields or []) | set(exclude or [])) - model_fields.keys()

        if invalid_fields:
            raise ValueError(
                f"Field(s) {invalid_fields} are not in pydantic model {model}"
            )

        for field_name in model_fields.keys():
            if field_name not in fields or field_name in exclude:
                continue

            yield all_fields[field_name]


factory = PartialFactory()
Partial = factory.create_schema
