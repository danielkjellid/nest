import functools
from typing import Any, Callable, TypeVar

from django.db.models import Model, QuerySet
from django.db.models import fields as django_fields
from django.db.models.fields import related as django_related_fields
from django.db import connection
from nest.core.exceptions import ApplicationError


def staff_required(func: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator that can be used alongside any endpoint to check if a user is staff.
    Will raise an ApplicationError with 401 if the user is not staff.
    """

    @functools.wraps(func)
    def inner(*args: Any, **kwargs: Any) -> Any:
        *_arg, info = args

        try:
            # Django ninja attaches the user object to the auth variable on the
            # request.
            user = info.auth

            if not user:
                raise ApplicationError(
                    message="User is unauthenticated.", status_code=401
                )

            if not user.is_staff:
                raise ApplicationError(message="User is not staff", status_code=401)

            return func(*args, **kwargs)
        except AttributeError as exc:
            raise AttributeError(
                "Auth attribute on WSGIRequest does not exist."
            ) from exc

    return inner


def ensure_no_fetch(func: Any):
    pre_run_queries = len(connection.queries)

    @functools.wraps(func)
    def inner(*args: Any, **kwargs: Any):
        print("HITS HERE")
        print(pre_run_queries)
        return func(*args, **kwargs)

    post_run_queries = len(connection.queries)

    if pre_run_queries != post_run_queries:
        raise RuntimeError("Caller was marked as no-fetch, but did a query.")

    return inner


T = TypeVar("T")


def ensure_prefetched_relations(  # noqa: C901
    *, arg_or_kwarg: str, skip_fields: list[str] | None = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
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

    fields_to_skip: list[str] = skip_fields if skip_fields else []

    def decorator(func: Any) -> Callable[..., T]:  # noqa: C901
        def inner(*args: Any, **kwargs: Any) -> Any:  # noqa: C901, PLR0912
            skip_check = kwargs.get("skip_check", False)

            if not skip_check:
                # We allow the instance we're checking to be passed both from args and
                # kwargs, so we need to find out which of them to use. For the args
                # part, it's highly likely that it's the first one that is of subclass
                # models.Model, but that is just an educated guess.
                arg_instance = next(
                    (arg for arg in args if issubclass(type(arg), Model)), None
                )
                # Look for defined arg_or_kwarg in passed kwargs.
                kwarg_instance = kwargs.get(arg_or_kwarg, None)

                # Attempt to find the instance we're looking for by either checking
                # selecting the first best option.
                instance_ = next(
                    (arg for arg in [arg_instance, kwarg_instance] if arg is not None),
                    None,
                )

                # If we don't find an instance to check on, raise error.
                if not instance_:
                    raise RuntimeError(
                        "Passed instance parameter was not found in neither args or "
                        "kwargs."
                    )

                # Iterate over all model fields, extracting the fields that we know
                # should be prefetched or selected.
                for field in instance_._meta.get_fields():
                    if (
                        isinstance(field, accepted_select_types)
                        and field.name not in fields_to_skip
                        and field.name not in fields_to_select
                    ):
                        fields_to_select.append(field.name)

                    if (
                        isinstance(field, accepted_prefetch_types)
                        and field.name not in fields_to_skip
                        and field.name not in fields_to_prefetch
                        # Also ignore fields that are marked for select here because a
                        # reverse 1-1 should be select_related, but OneToOne field is
                        # a child of ForeignKey with a unique constraint.
                        and field.name not in fields_to_select
                    ):
                        fields_to_prefetch.append(field.name)

                if len(fields_to_prefetch):
                    # Prefetched fields are stored in the _prefetched_objects_cache
                    # property, so check if that exists as long as we have fields that
                    # should be prefetched.
                    if not hasattr(instance_, "_prefetched_objects_cache"):
                        raise RuntimeError(
                            f"No relations seems to have been prefetched on "
                            f"{instance_}. Did you run .prefetch_related(...) on the "
                            f"queryset before passing the instance? "
                            f"Expected fields: {fields_to_prefetch}"
                        )

                    # Iterate over said fields and check if field name exists as a key
                    # in the _prefetched_objects_cache dict, if not, raise error.
                    for name in fields_to_prefetch:
                        if name not in instance_._prefetched_objects_cache.keys():
                            raise RuntimeError(
                                f"The relation {type(instance_)}.{name} on the "
                                f"instance {instance_} has not been prefetched. "
                                f"Unable to use method without using "
                                f'.prefetch_related("{name}") first.'
                            )

                    # Finally, clear the list to not retain data between runs.
                    fields_to_prefetch.clear()

                if len(fields_to_select):
                    # Selected related fields are stored in the _state.fields_cache
                    # property, so check if that exists as long as we have fields that
                    # should be select_related.
                    if not hasattr(instance_, "_state") or not hasattr(
                        instance_._state, "fields_cache"
                    ):
                        raise RuntimeError(
                            f"No relations seems to have been selected on {instance_}. "
                            f"Did you run .select_related(...) on the queryset before "
                            f"passing the instance? Expected fields: {fields_to_select}"
                        )

                    # Iterate over said fields and check if field name exists as a key
                    # in the fields_cache dict, if not, raise error.
                    for name in fields_to_select:
                        if name not in instance_._state.fields_cache.keys():
                            raise RuntimeError(
                                f"The relation {type(instance_)}.{name} on the "
                                f"instance {instance_} has not been selected. "
                                f"Unable to use method without using "
                                f'.select_related("{name}") first.'
                            )

                    fields_to_select.clear()

            return func(*args, **kwargs)

        return inner

    return decorator


def _ensure_prefetched_relations_for_instance(
    instance: Model, fields_to_skip: list[str]
):
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

    # Iterate over all model fields, extracting the fields that we know
    # should be prefetched or selected.
    for field in instance._meta.get_fields():
        if (
            isinstance(field, accepted_select_types)
            and field.name not in fields_to_skip
            and field.name not in fields_to_select
        ):
            fields_to_select.append(field.name)

        if (
            isinstance(field, accepted_prefetch_types)
            and field.name not in fields_to_skip
            and field.name not in fields_to_prefetch
            # Also ignore fields that are marked for select here because a
            # reverse 1-1 should be select_related, but OneToOne field is
            # a child of ForeignKey with a unique constraint.
            and field.name not in fields_to_select
        ):
            fields_to_prefetch.append(field.name)

    if len(fields_to_prefetch):
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
        for name in fields_to_prefetch:
            if name not in instance._prefetched_objects_cache.keys():
                raise RuntimeError(
                    f"The relation {type(instance)}.{name} on the "
                    f"instance {instance} has not been prefetched. "
                    f"Unable to use method without using "
                    f'.prefetch_related("{name}") first.'
                )

        # Finally, clear the list to not retain data between runs.
        fields_to_prefetch.clear()

    if len(fields_to_select):
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
        for name in fields_to_select:
            if name not in instance._state.fields_cache.keys():
                raise RuntimeError(
                    f"The relation {type(instance)}.{name} on the "
                    f"instance {instance} has not been selected. "
                    f"Unable to use method without using "
                    f'.select_related("{name}") first.'
                )

        fields_to_select.clear()


def ensure_prefetched_relations2(
    *, instance_or_qs: Model | QuerySet[Model], skip_fields: list[str] | None = None
):
    fields_to_skip: list[str] = skip_fields if skip_fields else []

    if isinstance(instance_or_qs, Model):
        _ensure_prefetched_relations_for_instance(
            instance=instance_or_qs, fields_to_skip=fields_to_skip
        )
    else:
        for instance in instance_or_qs:
            _ensure_prefetched_relations_for_instance(
                instance=instance, fields_to_skip=fields_to_skip
            )


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
