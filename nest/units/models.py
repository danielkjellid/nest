from django.db import models

from nest.core.models import BaseModel

from .enums import UnitType
from .managers import UnitQuerySet

_UnitManager = models.Manager.from_queryset(UnitQuerySet)


class Unit(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    name_pluralized = models.CharField(max_length=30, null=True)
    abbreviation = models.CharField(max_length=30, unique=True)
    unit_type = models.CharField(max_length=30, choices=UnitType.choices)
    base_factor = models.DecimalField(default=1, max_digits=10, decimal_places=2)
    is_base_unit = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)

    objects = _UnitManager()

    ADMIN_LIST_DISPLAY = ["name", "unit_type", "base_factor", "is_base_unit"]

    class Meta:
        verbose_name = "unit"
        verbose_name_plural = "units"

    def __str__(self) -> str:
        return self.name
