from typing import Type, TypeVar

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model

from nest.core.types import FetchedResult

from .models import LogEntry
from .records import LogEntryRecord

T_MODEL = TypeVar("T_MODEL", bound=Model)


def get_log_entries_for_object(
    *, model: Type[T_MODEL], pk: int, limit: int | None = None
) -> list[LogEntryRecord]:
    """
    Get a list of log entries based on generic model and pk.
    """
    log_entries = get_log_entries_for_objects(
        model=model,
        ids=[pk],
        limit=limit,
    )

    return log_entries[pk]


def get_log_entries_for_objects(
    *, model: Type[T_MODEL], ids: list[int], limit: int | None = None
) -> FetchedResult[list[LogEntryRecord]]:
    result: FetchedResult[list[LogEntryRecord]] = {}
    result_count: FetchedResult[int] = {}

    for pk in ids:
        result[pk] = []
        result_count[pk] = 0

    instance_content_type = ContentType.objects.get_for_model(model)
    log_entries = (
        LogEntry.objects.filter(content_type=instance_content_type, object_id__in=ids)
        .select_related("user")
        .order_by("-created_at")
    )

    for log_entry in log_entries:
        if limit and result_count[log_entry.object_id] >= limit:
            continue

        result[log_entry.object_id].append(
            LogEntryRecord(
                id=log_entry.id,
                action=log_entry.action,
                changes=log_entry.changes,
                user_or_source=_get_user_or_source(log_entry),
                remote_addr=log_entry.remote_addr,
                created_at=log_entry.created_at,
            )
        )

    return result


def _get_user_or_source(log_entry: LogEntry) -> str | None:
    user_or_source: str

    if log_entry.source is not None:
        user_or_source = log_entry.source
    elif log_entry.user is not None:
        user_or_source = log_entry.user.full_name
    else:
        user_or_source = None

    return user_or_source


def get_log_entries_for_instance(*, instance: T_MODEL) -> list[LogEntryRecord]:
    """
    Get a list of log entries based on a concrete instance.
    """

    if not isinstance(instance, Model):
        raise ValueError("The given instance is not a model instance.")

    instance_content_type = ContentType.objects.get_for_model(instance.__class__)

    log_entries = LogEntry.objects.filter(
        content_type=instance_content_type, object_id=instance.pk
    ).select_related("user__home")

    return [LogEntryRecord.from_log_entry(log_entry) for log_entry in log_entries]
