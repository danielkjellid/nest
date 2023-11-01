from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from nest.users.core.records import UserRecord

from .models import LogEntry


class LogEntryRecord(BaseModel):
    id: int
    action: int
    changes: dict[str, Any]
    user: UserRecord | None
    remote_addr: str | None
    source: str | None
    created_at: datetime

    @classmethod
    def from_log_entry(cls, log_entry: LogEntry) -> LogEntryRecord:
        return cls(
            id=log_entry.id,
            action=log_entry.action,
            changes=log_entry.changes,
            user=UserRecord.from_user(log_entry.user) if log_entry.user else None,
            remote_addr=log_entry.remote_addr,
            source=log_entry.source,
            created_at=log_entry.created_at,
        )
