from .models import LogEntry
from django.db.models import Model
from typing import TypeVar
from django.contrib.contenttypes.models import ContentType
from .records import LogEntryRecord

T_MODEL = TypeVar("T_MODEL", bound=Model)


def get_log_entries_for_object(*, model: T_MODEL, pk: int):
    instance_content_type = ContentType.objects.get_for_model(model)

    log_entries = LogEntry.objects.filter(
        content_type=instance_content_type, object_id=pk
    )

    return [LogEntryRecord.from_log_entry(log_entry) for log_entry in log_entries]


def get_log_entries_for_instance(*, instance: T_MODEL) -> list[LogEntryRecord]:
    if not isinstance(instance, Model):
        raise ValueError(message="The given instance is not a model instance.")

    instance_content_type = ContentType.objects.get_for_model(instance.__class__)

    log_entries = LogEntry.objects.filter(
        content_type=instance_content_type, object_id=instance.pk
    )

    return [LogEntryRecord.from_log_entry(log_entry) for log_entry in log_entries]
