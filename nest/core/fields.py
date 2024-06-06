from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

if TYPE_CHECKING:
    from pydantic import StrictBool, StrictInt, StrictStr
    from pydantic.typing import (
        AbstractSetIntStr,
        MappingIntStrAny,
        NoArgAnyCallable,
    )


def FormField(  # noqa
    default: Any = PydanticUndefined,
    *,
    default_factory: NoArgAnyCallable | None = None,
    alias: str | None = None,
    description: str | None = None,
    exclude: AbstractSetIntStr | MappingIntStrAny | Any | None = None,
    include: AbstractSetIntStr | MappingIntStrAny | Any | None = None,
    const: bool | None = None,
    gt: float | None = None,
    ge: float | None = None,
    lt: float | None = None,
    le: float | None = None,
    multiple_of: float | None = None,
    allow_inf_nan: bool | None = None,
    max_digits: int | None = None,
    decimal_places: int | None = None,
    min_items: int | None = None,
    max_items: int | None = None,
    unique_items: bool | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    allow_mutation: bool = True,
    regex: str | None = None,
    discriminator: str | None = None,
    repr: bool = True,
    title: str | None = None,
    component: str | None = None,
    default_value: StrictBool | StrictInt | StrictStr | None = None,
    placeholder: str | None = None,
    help_text: str | None = None,
    hidden_label: bool = False,
    col_span: int | None = None,
    section: str | None = None,
    order: int | None = 1,
    min: int | None = None,
    max: int | None = None,
    **extra: Any,
) -> Any:
    field_info = FieldInfo.from_field(
        default,
        default_factory=default_factory,
        alias=alias,
        title=title,
        description=description,
        exclude=exclude,
        include=include,
        const=const,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        min_items=min_items,
        max_items=max_items,
        unique_items=unique_items,
        min_length=min_length,
        max_length=max_length,
        allow_mutation=allow_mutation,
        regex=regex,
        discriminator=discriminator,
        repr=repr,
        help_text=help_text,
        component=component,
        default_value=default_value,
        placeholder=placeholder,
        hidden_label=hidden_label,
        col_span=col_span,
        section=section,
        order=order,
        min=min,
        max=max,
        **extra,
    )
    return field_info
