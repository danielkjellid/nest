from __future__ import annotations

import functools
from typing import Any, TypeVar, cast, Callable

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.http import HttpRequest
from django.utils.encoding import smart_str

from nest.core.utils import get_remote_request_ip, get_remote_request_user
from nest.users.models import User

from .models import LogEntry
from .utils import calculate_models_diff
from .records import LogEntryRecord

T = TypeVar("T")
T_MODEL = TypeVar("T_MODEL", bound=Model)


def log_create_or_updated(
    *,
    old: T_MODEL | None,
    new: T_MODEL,
    request_or_user: HttpRequest | User | None = None,
    source: str | None = None,
    ignore_fields: set[str] | None = None,
    is_updated: bool = False,
) -> LogEntryRecord:
    if ignore_fields is None:
        ignore_fields = set()

    IGNORED_FIELDS = {"updated_at", "created_at"} | ignore_fields

    fields = {
        field.name
        for field in new._meta.get_fields()
        if field.name not in IGNORED_FIELDS
    }

    if is_updated and old is None:
        old = new._meta.model.objects.get(pk=new.pk)

    diff = calculate_models_diff(old=old, new=new, fields=fields)
    user, request = None, None

    if request_or_user:
        user, request = get_remote_request_user(request_or_user=request_or_user)

    if old:
        created_log_entry = log_update(
            request=request, user=user, instance=new, changes=diff, source=source
        )
    else:
        created_log_entry = log_create(
            request=request, user=user, instance=new, changes=diff, source=source
        )

    return created_log_entry


def _create_log_entry(
    *,
    request: HttpRequest | None,
    instance: T_MODEL,
    user: User | None = None,
    changes: dict[str, tuple[T | None, T | None]] | None = None,
    action: int,
    **kwargs: Any,
) -> LogEntryRecord:
    """
    Helper function to create a new log entry. Changes should be in the format:
    changes = {
        'supplier': (<old_value>, <new_value>)
    }
    """

    remote_addr = None
    instance_pk = LogEntry.objects._get_pk_value(instance=instance)

    if changes is None:
        return None

    if request is not None:
        remote_addr = get_remote_request_ip(request=request)
        user = request.user if not user and isinstance(request.user, User) else user

    kwargs.setdefault("content_type", ContentType.objects.get_for_model(instance))
    kwargs.setdefault("object_repr", smart_str(instance))
    kwargs["changes"] = {}

    for key, (new_val, old_val) in changes.items():
        if isinstance(new_val, Model) and isinstance(old_val, Model):
            kwargs["changes"][key] = smart_str(new_val), smart_str(old_val)
        elif isinstance(new_val, Model):
            kwargs["changes"][key] = smart_str(new_val), old_val
        elif isinstance(old_val, Model):
            kwargs["changes"][key] = new_val, smart_str(old_val)
        else:
            kwargs["changes"][key] = new_val, old_val

    if isinstance(instance_pk, int):
        kwargs.setdefault("object_id", instance_pk)

    # Anonymous users can't be used
    if user and not user.is_authenticated:
        user = None

    log_entry = LogEntry.objects.create(
        user=user, remote_addr=remote_addr, action=action, **kwargs
    )

    return LogEntryRecord.from_log_entry(log_entry=log_entry)


log_create: Callable[..., LogEntryRecord] = functools.partial(
    _create_log_entry, action=LogEntry.ACTION_CREATE
)
log_update: Callable[..., LogEntryRecord] = functools.partial(
    _create_log_entry, action=LogEntry.ACTION_UPDATE
)
log_delete: Callable[..., LogEntryRecord] = functools.partial(
    _create_log_entry, action=LogEntry.ACTION_DELETE
)


class AuditLogger:
    """
    Context manager for audit logging. Find and store the difference between context
    enter and exit. Note that this only logs changes within the context.

    Usage:
    product = ...

    with AuditLogger(instance=product, request_or_user=request):
        ...
        product.title = "New title"
        product.save()
    """

    def __init__(
        self,
        instance: T_MODEL,
        include_fields: set[str] | None = None,
        exclude_fields: set[str] | None = None,
        request_or_user: HttpRequest | User | None = None,
    ) -> None:
        self.instance = instance
        self.request_or_user = request_or_user

        self.old_data: dict[str, str] = {}
        self.new_data: dict[str, str] = {}
        self.diff: dict[str, tuple[str, str]] = {}

        EXCLUDED_FIELDS = {"updated_at", "created_at"} | (exclude_fields or set())

        if include_fields:
            self.fields = include_fields
        else:
            self.fields = {
                field.name
                for field in instance._meta.get_fields()
                if field.name not in EXCLUDED_FIELDS
            }

    def _get_current_data_dict(self) -> dict[str, str]:
        """
        Get dict with current fields and values for the instance.

        I.e.: {"name": "Awesome product" ... }
        """

        return {
            field: smart_str(getattr(self.instance, field, None))
            for field in self.fields
        }

    def _get_and_set_diff(self) -> dict[str, tuple[str, str]]:
        """
        Get and set dict: keys as field names and values as a two-tuple with old value & new value.
        Uses previously stored data dict and new data dict to find the difference.

        I.e.: {"name": ("Awesome product", "Another awesome product") ... }
        """

        self.new_data = self._get_current_data_dict()

        _field_data = {
            field: (self.previous_data.get(field), self.new_data.get(field))
            for field in self.fields
        }
        self.diff = cast(
            dict[str, tuple[str, str]],
            {k: (old, new) for (k, (old, new)) in _field_data.items() if old != new},
        )
        return self.diff

    def __enter__(self) -> AuditLogger:
        """
        Store dict with previous data from the model instance as it is now.
        """

        self.previous_data = self._get_current_data_dict() if self.instance else {}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> AuditLogger:
        """
        On context exit: Find the difference, store it and create a LogEntry.
        """

        # Get the latest instance field data
        diff = self._get_and_set_diff()

        if not diff:
            # Nothing to do
            return self

        user, request = (
            get_remote_request_user(request_or_user=self.request_or_user)
            if self.request_or_user
            else (None, None)
        )

        # Log the difference
        if self.previous_data:
            log_update(request=request, user=user, instance=self.instance, changes=diff)
        else:
            log_create(request=request, user=user, instance=self.instance, changes=diff)

        return self
