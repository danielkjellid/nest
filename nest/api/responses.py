from typing import Generic, Literal, TypeVar, Any, Type
from pydantic.typing import display_as_type
from pydantic.generics import GenericModel

T = TypeVar("T")


class APIResponse(GenericModel, Generic[T]):
    status: Literal["success", "error"]
    message: str | None = None
    data: T | None

    @classmethod
    def __concrete_name__(cls: Type[Any], params: tuple[Type[Any], ...]) -> str:
        param_names = [display_as_type(param) for param in params]
        params_component = ", ".join(param_names)

        return (
            f"{params_component}APIResponse"
            if params_component != "NoneType"
            else "APIResponse"
        )
