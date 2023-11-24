from typing import Any, Iterable, Iterator, Type, TypeVar

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo, ModelField

M = TypeVar("M", bound=BaseModel)

__all__ = ["Partial", "Exclude"]


class PartialFactory:
    def partial(
        self,
        name: str | None,
        model: Type[M],
        fields: Iterable[str],
        overrides: dict[str, tuple[Type[Any], FieldInfo]] | None = None,
    ) -> Type[M]:
        return self.create_schema(
            name=name or model.__name__,
            model=model,
            fields=fields,
            overrides=overrides,
        )

    def exclude(
        self,
        name: str | None,
        model: Type[M],
        fields: Iterable[str],
        overrides: dict[str, tuple[Type[Any], FieldInfo]] | None = None,
    ) -> Type[M]:
        return self.create_schema(
            name=name or model.__name__,
            model=model,
            exclude=fields,
            overrides=overrides,
        )

    def create_schema(
        self,
        name: str,
        model: Type[M],
        fields: Iterable[str] | None = None,
        exclude: Iterable[str] | None = None,
        *,
        overrides: dict[str, tuple[Type[Any], FieldInfo]] | None = None,
        base_class: Type[BaseModel] = BaseModel,
    ) -> Type[M]:
        """
        Create a partial version of a pydantic model. Useful when only the partial data
        is needed.
        """

        definitions: dict[str, Any] = {}
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

        schema: Type[M] = create_model(  # type: ignore
            __model_name=name,
            __config__=None,
            __base__=base_class,
            __module__=base_class.__module__,
            __validators__=None,
            __cls_kwargs__=None,
            __slots__=None,
            **definitions,
        )

        return schema

    @staticmethod
    def _selected_pydantic_model_fields(
        model: Type[M],
        fields: Iterable[str] | None = None,
        exclude: Iterable[str] | None = None,
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
