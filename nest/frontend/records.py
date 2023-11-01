from pydantic import BaseModel

from nest.homes.records import HomeRecord
from nest.users.core.records import UserRecord


class FrontendMenuItemRecord(BaseModel):
    key: str
    title: str
    end: bool


class FrontendConfigRecord(BaseModel):
    is_production: bool


class FrontendInitialPropsRecord(BaseModel):
    menu: list[FrontendMenuItemRecord]
    config: FrontendConfigRecord
    current_user: UserRecord
    available_homes: list[HomeRecord]
