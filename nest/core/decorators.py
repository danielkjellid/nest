import functools
from typing import Any, Callable, TypeVar

from django.db.models import Model
from django.db.models import fields as django_fields
from django.db.models.fields import related as django_related_fields

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
