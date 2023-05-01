from typing import Iterable, TypeVar

from django.db.models import Model
from django.utils.encoding import smart_str

T_MODEL = TypeVar("T_MODEL", bound=Model)


def calculate_models_diff(
    old: T_MODEL | None, new: T_MODEL | None, fields: Iterable[str]
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
        old_value = smart_str(getattr(old, field, None))
        new_value = smart_str(getattr(new, field, None))

        if old_value != new_value:
            diff[field] = (smart_str(old_value), smart_str(new_value))

    if not diff:
        diff = None  # type: ignore

    return diff
