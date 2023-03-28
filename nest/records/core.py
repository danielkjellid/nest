from pydantic import BaseModel

from .homes import HomeRecord
from .users import UserRecord


class CoreMenuItemRecord(BaseModel):
    key: str
    title: str
    end: bool


class CoreConfigRecord(BaseModel):
    is_production: bool


class CoreInitialPropsRecord(BaseModel):
    menu: list[CoreMenuItemRecord]
    config: CoreConfigRecord
    current_user: UserRecord
    available_homes: list[HomeRecord]
