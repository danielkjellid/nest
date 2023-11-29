from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpRequest

if TYPE_CHECKING:
    from nest.users.core.models import User as UserModel
    from nest.users.core.types import User


def get_remote_request_ip(*, request: HttpRequest) -> str | None:
    """
    Returns a user's IP address if present in the request.
    """

    meta_fields = ["HTTP_X_FORWARDED_FOR", "REMOTE_ADDR"]

    for meta_field in meta_fields:
        meta_value = request.META.get(meta_field, None)
        if meta_value:
            return meta_value.split(",")[0]  # type: ignore

    return None


def get_remote_request_user(
    *, request_or_user: HttpRequest | UserModel | User
) -> tuple[User | None, HttpRequest | None]:
    """
    Get a user from request or passed user. Returned as a UserRecord.
    """
    from nest.users.core.models import User as UserModel
    from nest.users.core.types import User

    if isinstance(request_or_user, UserModel):
        return User.from_user(request_or_user), None

    if isinstance(request_or_user, User):
        return request_or_user, None

    if isinstance(request_or_user, HttpRequest):
        if request_or_user.user.is_anonymous:
            return None, request_or_user

        return (
            User.from_user(request_or_user.user),
            request_or_user,
        )

    raise ValueError("Please provide either an request or a user")
