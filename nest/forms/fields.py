from typing import TYPE_CHECKING, Any, Optional, Union
import inspect
from pydantic.fields import FieldInfo, UndefinedType

if TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr, MappingIntStrAny, NoArgAnyCallable

from nest.frontend.elements import FrontendElements
from .records import FormElementRecord

Undefined = UndefinedType()

element_record_field_kwargs = [key for key in FormElementRecord.__fields__.keys()]


def validate_element_record_fields_passed(func: Any):
    """
    Validate that all fields defined in FormElementRecord is available in the FormField
    function.
    """

    def inner(*args, **kwargs):
        acceptable_missing_param_keys = {"id", "type", "enum", "parent"}
        element_record_keys = (
            set(element_record_field_kwargs) - acceptable_missing_param_keys
        )
        signature_param_keys = set(list(inspect.signature(func).parameters.keys()))

        assert element_record_keys <= signature_param_keys, (
            f"Some FormElementRecord fields are missing as parameters in FormField "
            f"function."
        )
        return func(*args, **kwargs)

    return inner


@validate_element_record_fields_passed
def FormField(
    default: Any = Undefined,
    *,
    default_factory: Optional["NoArgAnyCallable"] = None,
    alias: str = None,
    description: str = None,
    exclude: Union["AbstractSetIntStr", "MappingIntStrAny", Any] = None,
    include: Union["AbstractSetIntStr", "MappingIntStrAny", Any] = None,
    const: bool = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    multiple_of: float = None,
    allow_inf_nan: bool = None,
    max_digits: int = None,
    decimal_places: int = None,
    min_items: int = None,
    max_items: int = None,
    unique_items: bool = None,
    min_length: int = None,
    max_length: int = None,
    allow_mutation: bool = True,
    regex: str = None,
    discriminator: str = None,
    repr: bool = True,
    title: str = None,
    element: FrontendElements = None,
    placeholder: str = None,
    help_text: str | None = None,
    hidden_label: bool = False,
    col_span: int = None,
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
