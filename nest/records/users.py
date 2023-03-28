from __future__ import annotations

from pydantic import BaseModel

from nest.models import User

from .homes import HomeRecord


class UserRecord(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    full_name: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    home: HomeRecord | None

    @classmethod
    def from_user(cls, user: User, include_home: bool = False) -> UserRecord:
        """
        Generate a record from the user model. Note that passing the include_home param
        will cause an additional lookup, so it's not advised to do that in a loop.
        """
        return cls(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser,
            home=(HomeRecord.from_home(user.home) if user.home else None)
            if include_home
            else None,
        )
