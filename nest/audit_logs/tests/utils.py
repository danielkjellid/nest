from typing import Any, TypeVar

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model

from nest.audit_logs.models import LogEntry
from nest.users.core.models import User

T_MODEL = TypeVar("T_MODEL", bound=Model)


def create_log_entry(
    *,
    instance: T_MODEL,
    user: User | None = None,
    action: int = LogEntry.ACTION_UPDATE,
    changes: dict[str, tuple[Any | None, Any | None]],
) -> LogEntry:
    """
    Create a log entry used for testing purposes.
    """
    content_type = ContentType.objects.get_for_model(instance.__class__)
    log_entry = LogEntry.objects.create(
        content_type=content_type,
        object_id=instance.pk,
        action=action,
        user=user,
        changes=changes,
    )

    return log_entry
