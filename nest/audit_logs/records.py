from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from .models import LogEntry


class LogEntryRecord(BaseModel):
    id: int
    action: int
    changes: dict[str, Any]
    user_or_source: str | None
    remote_addr: str | None
    created_at: datetime

    @classmethod
    def from_log_entry(cls, log_entry: LogEntry) -> LogEntryRecord:
        user_or_source: str | None

        if log_entry.source is not None:
            user_or_source = log_entry.source
        elif log_entry.user is not None:
            user_or_source = log_entry.user.full_name
        else:
            user_or_source = None

        return cls(
            id=log_entry.id,
            action=log_entry.action,
            changes=log_entry.changes,
            user_or_source=user_or_source,
            remote_addr=log_entry.remote_addr,
            created_at=log_entry.created_at,
        )
