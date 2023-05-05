from typing import Any, TypeVar

from django.db.models import ManyToManyField, Model
from django.http import HttpRequest

from nest.audit_logs.services import log_update

T = TypeVar("T", bound=Model)


def model_update(
    *,
    instance: T,
    fields: list[str],
    data: dict[str, Any],
    request: HttpRequest | None = None,
    log_change: bool = True,
    log_ignore_fields: set[str] | None = None,
) -> tuple[T, bool]:
    """
    Generic update service meant to be reused in local update services.

    For example:

    def user_update(*, user: User, data) -> User:
        fields = ['first_name', 'last_name']
        user, has_updated = model_update(instance=user, fields=fields, data=data)

        // Do other actions with the user here

        return user

    Return value: Tuple with the following elements:
        1. The instance we updated.
        2. A boolean value representing whether we performed an update or not.

    Some important notes:
        - Only keys present in `fields` will be taken from `data`.
        - If something in present in `fields` but not present in `data`, we simply skip.
        - There's a strict assertion that all values in `fields` are actual fields in `instance`.
        - `fields` can support m2m fields, which are handled after the update on `instance`.
        - If `auto_updated_at` is True, we'll try bumping `updated_at` with the current timestamp.
    """

    has_updated = False
    m2m_data = {}
    update_fields = []
    changes = {}

    if log_ignore_fields is None:
        log_ignore_fields = set()

    model_fields = {field.name: field for field in instance._meta.get_fields()}

    for field in fields:
        if field not in data:
            continue

        model_field = model_fields.get(field, None)

        assert (
            model_field is not None
        ), f"{field} is not part of {instance.__class__.__name__} fields."

        # If we have m2m field, handle differently
        if isinstance(model_field, ManyToManyField):
            m2m_data[field] = data[field]
            continue

        instance_field_val = getattr(instance, field)
        if instance_field_val != data[field]:
            has_updated = True
            update_fields.append(field)
            setattr(instance, field, data[field])

            if field not in log_ignore_fields:
                changes[field] = (instance_field_val, data[field])

    if has_updated:
        instance.full_clean()
        instance.save(update_fields=update_fields)

        if log_change:
            log_update(instance=instance, request=request, changes=changes)

    for field_name, value in m2m_data.items():
        related_manager = getattr(instance, field_name)
        related_manager.set(value)
        has_updated = True

    return instance, has_updated
