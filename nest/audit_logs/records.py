from __future__ import annotations
from pydantic import BaseModel
from nest.users.records import UserRecord
from .models import LogEntry
from typing import Any


class LogEntryRecord(BaseModel):
    id: int
    action: LogEntry.ACTIONS
    changes: dict[str, Any]
    user: UserRecord | None
    remote_addr: str
    source: str

    @classmethod
    def from_log_entry(cls, log_entry: LogEntry) -> LogEntryRecord:
        return cls(
            id=log_entry.id,
            action=log_entry.action,
            changes=log_entry.changes,
            user=UserRecord.from_user(log_entry.user) if log_entry.user else None,
            remote_addr=log_entry.remote_addr,
            source=log_entry.source,
        )
