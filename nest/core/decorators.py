import functools
from typing import Any, Callable

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
