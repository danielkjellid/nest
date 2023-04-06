from typing import Generic, Literal, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class APIResponse(GenericModel, Generic[T]):
    status: Literal["success", "error"]
    message: str | None = None
    data: T | None
