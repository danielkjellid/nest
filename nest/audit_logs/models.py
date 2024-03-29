from typing import ClassVar

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from nest.core.models import BaseModel

from .managers import LogEntryManager, LogEntryQuerySet

_LogEntryManager = LogEntryManager.from_queryset(LogEntryQuerySet)


class LogEntry(BaseModel):
    ACTION_CREATE = 0
    ACTION_UPDATE = 1
    ACTION_DELETE = 2

    ACTIONS = (
        (ACTION_CREATE, "create"),
        (ACTION_UPDATE, "update"),
        (ACTION_DELETE, "delete"),
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="log content type",
    )
    object_repr = models.TextField()
    object_id = models.BigIntegerField(
        blank=True, db_index=True, null=True, verbose_name="log object id"
    )
    content_object = GenericForeignKey("content_type", "object_id")
    action = models.PositiveSmallIntegerField(choices=ACTIONS, verbose_name="action")
    changes = models.JSONField(encoder=DjangoJSONEncoder, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    remote_addr = models.GenericIPAddressField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    objects = _LogEntryManager()

    class Meta:
        get_latest_by = "created_at"
        ordering: ClassVar = ["-created_at"]
        verbose_name = "log entry"
        verbose_name_plural = "log entries"
