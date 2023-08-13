from __future__ import annotations

from pydantic import BaseModel

from nest.homes.records import HomeRecord
from nest.users.models import User
from nest.core.utils import ensure_prefetched_relations


class UserRecord(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    full_name: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    is_hijacked: bool = False
    home: HomeRecord | None

    @classmethod
    def from_user(cls, user: User, skip_check: bool = False) -> UserRecord:
        if not skip_check:
            ensure_prefetched_relations(instance=user, prefetch_keys=["home"])

        is_hijacked = getattr(user, "is_hijacked", False)

        return cls(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser,
            is_hijacked=is_hijacked,
            home=HomeRecord.from_home(user.home) if user.home else None,
        )
