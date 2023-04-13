from pydantic import BaseModel

from nest.homes.records import HomeRecord
from nest.users.records import UserRecord


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
