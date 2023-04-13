from typing import TYPE_CHECKING, Any

from django.contrib.auth.models import BaseUserManager

from nest.core.managers import BaseQuerySet

if TYPE_CHECKING:
    from .models import User  # noqa


class UserQuerySet(BaseQuerySet["User"]):
    pass


class UserManager(BaseUserManager["User"]):
    """
    Default manager for the User model.
    """

    def create_user(self, *args: Any, **kwargs: Any) -> None:
        """Create a user"""
        raise RuntimeError("Please use the create_user service")

    def create_superuser(self, *args: Any, **kwargs: Any) -> None:
        """Create a superuser"""
        raise RuntimeError("Please use the create_user service")
