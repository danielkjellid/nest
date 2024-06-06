from __future__ import annotations

from types import NoneType, UnionType
from typing import Any, Generic, Literal, Type, TypeVar, get_origin, get_args

from pydantic.generics import GenericModel

T = TypeVar("T")


def _build_name_from_inner_list_type(
    t_type: T, cls: Type[APIResponse[T]], mid_fix: str = ""
) -> str:
    assert get_origin(t_type) in (list, set, tuple)
    t_type_inner = get_args(t_type)[0]
    return f"{t_type_inner.__name__}{mid_fix.capitalize()}{cls.__name__}"


def _build_name(t_type: T, cls: Type[APIResponse[T]]) -> str:
    """
    Build a parameterized name for a model or list of models.
    """
    if (
        get_origin(t_type) is list
        or get_origin(t_type) is set
        or get_origin(t_type) is tuple
    ):
        return _build_name_from_inner_list_type(t_type, cls, mid_fix="list")
    elif get_origin(t_type) is UnionType:
        args = get_args(t_type)
        is_optional = any(arg is NoneType for arg in args)
        required_args = [arg for arg in args if arg is not NoneType]

        if len(required_args) > 1:
            raise RuntimeError(
                "Got multiple required types in union type, not sure how to "
                "concatenate a good parameterized name for model"
            )
        if is_optional:
            name = _build_name(required_args[0], cls)
            return f"Optional{name}"
        else:
            return _build_name(required_args[0], cls)
    elif get_origin(t_type) is NoneType:
        return "FOOOO"
    else:
        return f"{t_type.__name__}{cls.__name__}"  # type: ignore


class APIResponse(GenericModel, Generic[T]):
    status: Literal["success", "error"]
    message: str | None = None
    data: T | None

    @classmethod
    def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:
        if not params:
            return cls.__name__

        # We want the first parameter passed into the generic model, e.g. the "T".
        t_type = params[0]
        try:
            return _build_name(t_type, cls)
        except AttributeError:
            return "FOOO"
