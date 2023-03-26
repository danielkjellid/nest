from pydantic import BaseModel
from .users import UserRecord
from .homes import HomeRecord


class CoreConfigRecord(BaseModel):
    is_production: bool


class CoreInitialPropsRecord(BaseModel):
    config: CoreConfigRecord
    current_user: UserRecord
    available_homes: list[HomeRecord]
