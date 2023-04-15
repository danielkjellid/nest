import typing

import pydantic


def is_list(*, obj: typing.Any) -> bool:
    return typing.get_origin(obj) is list


def is_pydantic_model(*, obj: typing.Any) -> bool:
    return issubclass(obj, pydantic.BaseModel) or (
        hasattr(obj, "__pydantic_model__")
        and issubclass(obj.__pydantic_model__, pydantic.BaseModel)
    )


def get_inner_list_type(*, obj: typing.Any) -> tuple[type, bool]:
    is_lst = is_list(obj=obj)
    if is_lst:
        obj = unwrap_item_type_from_list(obj=obj)
    return obj, is_lst


def unwrap_item_type_from_list(*, obj: typing.Any) -> type:
    return typing.get_args(obj)[0]  # type: ignore
