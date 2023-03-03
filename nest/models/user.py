from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.db import models

from typing import Any
from django.contrib.auth.models import BaseUserManager
from .base import BaseQuerySet, BaseModel


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


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    first_name = models.CharField(
        max_length=255,
        unique=False,
    )
    last_name = models.CharField(
        max_length=255,
        unique=False,
    )
    is_active = models.BooleanField()
    is_superuser = models.BooleanField()

    USERNAME_FIELD = "email"

    objects = UserManager.from_queryset(UserQuerySet)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
