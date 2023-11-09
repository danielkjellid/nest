import functools
from typing import Any, Callable

import structlog

from nest.core.exceptions import ApplicationError

logger = structlog.get_logger()


def staff_required(func: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator that can be used alongside any endpoint to check if a user is staff.
    Will raise an ApplicationError with 401 if the user is not staff.
    """

    @functools.wraps(func)
    def inner(*args: Any, **kwargs: Any) -> Any:
        *_arg, info = args

        # try:
        # Django ninja attaches the user object to the auth variable on the
        # request.
        user = getattr(info, "auth", None)

        if not user:
            logger.warning(
                "User was resolved to None, auth attribute on WSGIRequest might "
                "possibly not exist.",
                user=user,
                info=info,
            )
            raise ApplicationError(message="User is unauthenticated.", status_code=401)

        if not user.is_staff:
            raise ApplicationError(message="User is not staff", status_code=401)

        return func(*args, **kwargs)

    return inner
