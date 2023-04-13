from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models

from .enums import AvatarColors

from nest.core.models import BaseModel
from .managers import UserManager, UserQuerySet


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
    avatar_color = models.CharField(
        max_length=8,
        unique=False,
        choices=AvatarColors.choices,
    )
    home = models.ForeignKey(
        "homes.Home",
        related_name="residents",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    homes = models.ManyToManyField("homes.Home", related_name="users", blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager.from_queryset(UserQuerySet)()

    USERNAME_FIELD = "email"
    ADMIN_LIST_DISPLAY = (
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
