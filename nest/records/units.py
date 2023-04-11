from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel

from nest.enums import UnitType
from nest.models import Unit


class UnitRecord(BaseModel):
    id: int
    name: str
    name_pluralized: str | None
    abbreviation: str
    unit_type: UnitType
    base_factor: Decimal
    is_base_unit: bool
    is_default: bool

    @classmethod
    def from_unit(cls, unit: Unit) -> UnitRecord:
        return cls(
            id=unit.id,
            name=unit.name,
            name_pluralized=unit.name_pluralized,
            abbreviation=unit.abbreviation,
            unit_type=unit.unit_type,
            base_factor=unit.base_factor,
            is_base_unit=unit.is_base_unit,
            is_default=unit.is_default,
        )
