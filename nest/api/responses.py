from pydantic.generics import GenericModel
from ninja import Schema
from typing import Literal, TypeVar, Generic

T = TypeVar("T", bound=list[Schema] | Schema)


class APIResponse(GenericModel, Generic[T]):
    status: Literal["success", "error"]
    message: str | None = None
    data: T | None
