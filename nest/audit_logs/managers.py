from __future__ import annotations
from typing import TYPE_CHECKING, Any

from django.db.models import Model, Manager

from nest.core.managers import BaseQuerySet

if TYPE_CHECKING:
    from nest.audit_logs import models  # noqa


class LogEntryManager(Manager):
    def _get_pk_value(self, instance: Model) -> Any:
        """
        Get the primary key field value for a specific model instance.
        """

        pk_field = instance._meta.pk.name
        pk = getattr(instance, pk_field, None)

        # Make sure that a pk is returned, and not a model instance.
        if isinstance(pk, Model):
            pk = self._get_pk_value(pk)

        return pk


class LogEntryQuerySet(BaseQuerySet["models.LogEntry"]):
    ...
