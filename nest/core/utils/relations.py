from django.db.models import Model
from django.db.models import fields as django_fields
from django.db.models.fields import related as django_related_fields


def get_related_field(instance: Model, model_field: str):
    fields_to_prefetch: list[str] = []
    accepted_prefetch_types = (
        django_fields.reverse_related.ManyToManyRel,
        django_fields.reverse_related.ManyToOneRel,
        django_fields.reverse_related.ForeignObjectRel,
    )

    fields_to_select: list[str] = []
    accepted_select_types = (
        django_related_fields.ForeignKey,
        django_related_fields.OneToOneField,
        django_fields.reverse_related.OneToOneRel,
    )

    fields = instance._meta.get_fields()

    # Iterate over all model fields, extracting the fields that we know
    # should be prefetched or selected.
    for field in fields:
        if (
            isinstance(field, accepted_select_types)
            and field.name not in fields_to_select
        ):
            fields_to_select.append(field.name)

        if (
            isinstance(field, accepted_prefetch_types)
            and field.name not in fields_to_prefetch
            # Also ignore fields that are marked for select here because a
            # reverse 1-1 should be select_related, but OneToOne field is
            # a child of ForeignKey with a unique constraint.
            and field.name not in fields_to_select
        ):
            fields_to_prefetch.append(field.name)

    # If model has no relations, just return the field.
    if not fields_to_prefetch and not fields_to_select:
        return getattr(instance, model_field)

    if len(fields_to_prefetch) and model_field in fields_to_prefetch:
        # Prefetched fields are stored in the _prefetched_objects_cache
        # property, so check if that exists as long as we have fields that
        # should be prefetched.
        if not hasattr(instance, "_prefetched_objects_cache"):
            raise RuntimeError(
                f"No relations seems to have been prefetched on "
                f"{instance}. Did you run .prefetch_related(...) on the "
                f"queryset before passing the instance? "
                f"Expected fields: {fields_to_prefetch}"
            )

        # Iterate over said fields and check if field name exists as a key
        # in the _prefetched_objects_cache dict, if not, raise error.
        if model_field not in instance._prefetched_objects_cache.keys():
            raise RuntimeError(
                f"The relation {type(instance)}.{model_field} on the "
                f"instance {instance} has not been prefetched. "
                f"Unable to use method without using "
                f'.prefetch_related("{model_field}") first.'
            )

        # Finally, clear the list to not retain data between runs.
        fields_to_prefetch.clear()

    if len(fields_to_select) and model_field in fields_to_select:
        # Selected related fields are stored in the _state.fields_cache
        # property, so check if that exists as long as we have fields that
        # should be select_related.
        if not hasattr(instance, "_state") or not hasattr(
            instance._state, "fields_cache"
        ):
            raise RuntimeError(
                f"No relations seems to have been selected on {instance}. "
                f"Did you run .select_related(...) on the queryset before "
                f"passing the instance? Expected fields: {fields_to_select}"
            )

        # Iterate over said fields and check if field name exists as a key
        # in the fields_cache dict, if not, raise error.
        if model_field not in instance._state.fields_cache.keys():
            raise RuntimeError(
                f"The relation {type(instance)}.{model_field} on the "
                f"instance {instance} has not been selected. "
                f"Unable to use method without using "
                f'.select_related("{model_field}") first.'
            )

        fields_to_select.clear()

    return getattr(instance, model_field)
