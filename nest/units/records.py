from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel

from .enums import UnitType
from .models import Unit


class UnitRecord(BaseModel):
    id: int
    name: str
    name_pluralized: str | None = None
    abbreviation: str
    unit_type: UnitType
    base_factor: Decimal
    is_base_unit: bool
    is_default: bool
    display_name: str | None = None

    @classmethod
    def from_unit(cls, unit: Unit) -> UnitRecord:
        return cls(
            id=unit.id,
            name=unit.name,
            name_pluralized=unit.name_pluralized,
            abbreviation=unit.abbreviation,
            unit_type=UnitType(unit.unit_type),
            base_factor=unit.base_factor,
            is_base_unit=unit.is_base_unit,
            is_default=unit.is_default,
            display_name=getattr(unit, "display_name", None),
        )
