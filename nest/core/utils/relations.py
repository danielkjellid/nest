from typing import TypeVar
from django.db.models import Model

T = TypeVar("T", bound=Model)


def ensure_prefetched_relations(*, instance: T, prefetch_keys: list[str]):
    """
    Utility to ensure that a prefetch has been made. Useful in records which populates
    other records across relations to ensure that we do not end up in an n+1 scenario.
    """
    if not prefetch_keys:
        raise RuntimeError("prefetch_keys kwarg cannot be an empty list.")

    for key in prefetch_keys:
        found_prefetched_value = False
        found_related_value = False

        model_fields = {field.name for field in instance._meta.get_fields()}

        if key not in model_fields:
            raise RuntimeError(
                f"The field {key} does not exist on the "
                f"{instance._meta.model} model."
            )

        if hasattr(instance, "_prefetched_objects_cache"):
            if key in instance._prefetched_objects_cache.keys():
                found_prefetched_value = True

        if hasattr(instance, "_state") and hasattr(instance._state, "fields_cache"):
            if key in instance._state.fields_cache:
                found_related_value = True

        if not found_prefetched_value and not found_related_value:
            raise RuntimeError(
                f"The relation {key} has not been prefetched. "
                f'Unable to use method without using .select_related("{key}")/'
                f'.prefetch_related("{key}") first.'
            )
