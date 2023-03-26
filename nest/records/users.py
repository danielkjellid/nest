from __future__ import annotations

from pydantic import BaseModel
from .homes import HomeRecord
from nest.models import User


class UserRecord(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    full_name: str
    is_active: bool
    is_superuser: bool
    home: HomeRecord | None

    @classmethod
    def from_user(cls, user: User) -> UserRecord:
        return cls(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            home=HomeRecord.from_home(user.home),
        )
