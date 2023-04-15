from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, Callable

from pydantic.fields import FieldInfo, UndefinedType

if TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr, MappingIntStrAny, NoArgAnyCallable

from nest.frontend.elements import FrontendElements

from .records import FormElementRecord

Undefined = UndefinedType()

element_record_field_kwargs = list(FormElementRecord.__fields__.keys())


def validate_element_record_fields_passed(func: Callable[..., Any]) -> Any:
    """
    Validate that all fields defined in FormElementRecord is available in the FormField
    function.
    """

    def inner(*args: Any, **kwargs: Any) -> Any:
        acceptable_missing_param_keys = {"id", "type", "enum", "parent"}
        element_record_keys = (
            set(element_record_field_kwargs) - acceptable_missing_param_keys
        )
        signature_param_keys = set(inspect.signature(func).parameters.keys())

        assert element_record_keys <= signature_param_keys, (
            "Some FormElementRecord fields are missing as parameters in FormField "
            "function."
        )
        return func(*args, **kwargs)

    return inner


@validate_element_record_fields_passed
def FormField(
    default: Any = Undefined,
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
    element: FrontendElements | None = None,
    placeholder: str | None = None,
    help_text: str | None = None,
    hidden_label: bool = False,
    col_span: int | None = None,
    section: str | None = None,
    **extra: Any,
) -> Any:
    field_info = FieldInfo(
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
        element=element,
        placeholder=placeholder,
        hidden_label=hidden_label,
        col_span=col_span,
        section=section,
        **extra,
    )
    field_info._validate()
    return field_info
