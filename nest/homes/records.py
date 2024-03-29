from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel

from .models import Home


class HomeRecord(BaseModel):
    id: int
    address: str
    num_residents: int
    num_weeks_recipe_rotation: int
    weekly_budget: Decimal
    is_active: bool

    @classmethod
    def from_home(cls, home: Home) -> HomeRecord:
        return cls(
            id=home.id,
            address=home.address,
            num_residents=home.num_residents,
            num_weeks_recipe_rotation=home.num_weeks_recipe_rotation,
            weekly_budget=home.weekly_budget,
            is_active=home.is_active,
        )
