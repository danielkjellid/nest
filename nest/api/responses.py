from typing import Any, Generic, Literal, Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


def display_as_type(v: Type[Any]) -> str:
    try:
        return v.__name__
    except AttributeError:
        # happens with typing objects
        return str(v).replace("typing.", "")


class APIResponse(BaseModel, Generic[T]):
    status: Literal["success", "error"]
    message: str | None = None
    data: T | None

    @classmethod
    def __concrete_name__(cls: Type[Any], params: tuple[Type[Any], ...]) -> str:
        param_names = [display_as_type(param) for param in params]
        params_component = ", ".join(param_names)

        # Nested types, such as lists gets annotated like list[path.to.ActualType],
        # as we only want the outer + actual type, slice string appropriately and get
        # it. For example, when passed a list[Record], we want the generated name to be
        # RecordListAPIResponse, otherwise RecordAPIResponse will suffice.
        if "[" in params_component and "]" in params_component:
            inner_type = params_component[
                params_component.find("[") + 1 : params_component.find("]")
            ]
            outer_type = (
                params_component.replace(inner_type, "")
                .replace("[", "")
                .replace("]", "")
            )

            params_component = f"{inner_type.split('.')[-1]}{outer_type.capitalize()}"

        return (
            f"{params_component}APIResponse"
            if params_component != "NoneType"
            else "APIResponse"
        )
