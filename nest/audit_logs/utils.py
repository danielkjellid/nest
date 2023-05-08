from decimal import Decimal
from typing import Any, Iterable

from django.db.models import Model
from django.utils.encoding import smart_str


def calculate_models_diff(
    old: Model | None, new: Model | None, fields: Iterable[str]
) -> dict[str, tuple[str | None, str | None]] | None:
    """
    Calculates the differences between two model instances. One of the
    instances may be None (i.e., a newly created model or deleted model). This
    will cause all fields with a value to have changed (from None).
    """

    if not (old is None or isinstance(old, Model)):
        raise TypeError("The supplied old instance is not a valid model instance.")
    if not (new is None or isinstance(new, Model)):
        raise TypeError("The supplied new instance is not a valid model instance.")

    diff = {}

    for field in fields:
        old_value = smart_str(getattr(old, field, None), strings_only=True)
        new_value = smart_str(getattr(new, field, None), strings_only=True)

        if old_value != new_value:
            if isinstance(old_value, Decimal) and isinstance(new_value, str):
                if old_value == Decimal(new_value):
                    continue

            elif isinstance(new_value, Decimal) and isinstance(old_value, str):
                if Decimal(old_value) == new_value:
                    continue

            diff[field] = (smart_str(old_value), smart_str(new_value))

    if not diff:
        diff = None  # type: ignore

    return diff


def format_changes_display(
    *, changes: dict[str, tuple[Any | None, Any | None]]
) -> list[str]:
    formatted_changes = [
        f"{key} changed from {old_value} to {new_value}"
        for key, (old_value, new_value) in changes.items()
    ]

    return formatted_changes
