import functools
from typing import Any, Callable
from django.db.models import Model, fields as django_fields
from django.db.models.fields.related import ForeignKey, OneToOneRel
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


def ensure_prefetched_relations(*, instance: str, skip_fields: list | None = None):
    fields_to_prefetch = []
    accepted_prefetch_types = (
        django_fields.reverse_related.ManyToManyRel,
        django_fields.reverse_related.ManyToOneRel,
    )

    fields_to_select = []
    accepted_select_types = (ForeignKey, OneToOneRel)

    if not skip_fields:
        skip_fields = []

    def decorator(func: Any):
        def inner(*args: Any, **kwargs: Any):
            skip_check = kwargs.get("skip_check", False)

            if not skip_check:
                arg_instance = next(
                    (arg for arg in args if issubclass(type(arg), Model)), None
                )
                kwarg_instance = kwargs.get(instance, None)
                instance_ = next(
                    (arg for arg in [arg_instance, kwarg_instance] if arg is not None),
                    None,
                )

                if not instance_:
                    raise RuntimeError(
                        "Passed instance parameter was not found in neither args or "
                        "kwargs."
                    )

                for field in instance_._meta.get_fields():
                    if (
                        isinstance(field, accepted_prefetch_types)
                        and field.name not in skip_fields
                    ):
                        fields_to_prefetch.append(field.name)

                    if (
                        isinstance(field, accepted_select_types)
                        and field.name not in skip_fields
                    ):
                        fields_to_select.append(field.name)

                if len(fields_to_prefetch) and not hasattr(
                    instance_, "_prefetched_objects_cache"
                ):
                    raise RuntimeError(
                        f"No relations seems to have been prefetched on {instance_}. "
                        f"Did you run .prefetch_related(...) on the queryset before "
                        f"passing the instance? Expected fields: {fields_to_prefetch}"
                    )

                for name in fields_to_prefetch:
                    if name not in instance_._prefetched_objects_cache.keys():
                        raise RuntimeError(
                            f"The relation {type(instance_)}.{name} on the instance "
                            f"{instance_} has not been prefetched. Unable to use "
                            f'method without using .prefetch_related("{name}") first.'
                        )

                fields_to_prefetch.clear()

                if len(fields_to_select) and (
                    not hasattr(instance_, "_state")
                    or not hasattr(instance_._state, "fields_cache")
                ):
                    raise RuntimeError(
                        f"No relations seems to have been selected on {instance_}. "
                        f"Did you run .select_related(...) on the queryset before "
                        f"passing the instance? Expected fields: {fields_to_select}"
                    )

                for name in fields_to_select:
                    if name not in instance_._state.fields_cache:
                        raise RuntimeError(
                            f"The relation {type(instance_)}.{name} on the instance "
                            f"{instance_} has not been selected. Unable to use method "
                            f'without using .select_related("{name}") first.'
                        )

                fields_to_select.clear()

            return func(*args, **kwargs)

        return inner

    return decorator


def ensure_annotated_values(*, instance: str, annotations: list[str]):
    missing_annotations: []

    def decorator(func: Any):
        def inner(*args: Any, **kwargs: Any):
            skip_check = kwargs.get("skip_check", False)

            if not skip_check:
                arg_instance = next(
                    (arg for arg in args if issubclass(type(arg), Model)), None
                )
                kwarg_instance = kwargs.get(instance, None)
                instance_ = next(
                    (arg for arg in [arg_instance, kwarg_instance] if arg is not None),
                    None,
                )

                if not instance_:
                    raise RuntimeError(
                        "Passed instance parameter was not found in neither args or "
                        "kwargs."
                    )

                model_fields = set(field.name for field in instance_._meta.get_fields())
                annotations_to_check = set(annotations) - model_fields

                for annotation in annotations_to_check:
                    if not hasattr(instance_, annotation):
                        missing_annotations.append(annotation)

                if len(missing_annotations):
                    raise RuntimeError(
                        f"Instance {instance_} is missing one or more annotations. "
                        f"Expected annotated values: {missing_annotations}"
                    )

                missing_annotations.clear()

            return func(*args, **kwargs)

        return inner

    return decorator
