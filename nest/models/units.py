from __future__ import annotations
from django.db import models
from nest.enums import Unit
from .base import BaseModel, BaseQuerySet


class UnitQuerySet(BaseQuerySet["Unit"]):
    ...


_UnitManager = models.Manager.from_queryset(UnitQuerySet)


class Unit(BaseModel):
    name = models.CharField(max_length=30)
    name_pluralized = models.CharField(max_length=30, null=True)
    abbreviation = models.CharField(max_length=30)
    unit_type = models.CharField(max_length=30, choices=Unit.choices)
    base_factor = models.DecimalField(default=1, max_digits=10, decimal_places=2)
    is_base_unit = models.BooleanField(default=False)

    objects = _UnitManager()

    ADMIN_LIST_DISPLAY = ["name", "unit_type", "base_factor", "is_base_unit"]

    class Meta:
        verbose_name = "unit"
        verbose_name_plural = "units"

    def __str__(self) -> str:
        return self.name
