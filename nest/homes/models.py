from django.db import models

from nest.core.models import BaseModel

from .managers import HomeQuerySet

_HomeManager = models.Manager.from_queryset(HomeQuerySet)


class Home(BaseModel):
    street_address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    zip_place = models.CharField(max_length=50)
    num_residents = models.BigIntegerField()
    num_weeks_recipe_rotation = models.BigIntegerField(default=2)
    weekly_budget = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    objects = _HomeManager()

    ADMIN_LIST_DISPLAY = ["street_address", "zip_code", "zip_place", "is_active"]

    class Meta:
        verbose_name = "home"
        verbose_name_plural = "homes"

    def __str__(self) -> str:
        return self.address

    @property
    def address(self) -> str:
        return f"{self.street_address}, {self.zip_code} {self.zip_place}"
