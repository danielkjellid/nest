from typing import Any, Callable

import pytest

from nest.units.enums import UnitType
from nest.units.models import Unit

UNITS = {
    "pcs": dict(
        name="Piece",
        name_pluralized="Pieces",
        abbreviation="pcs",
        unit_type=UnitType.PIECES,
        base_factor="1.00",
        is_base_unit=True,
        is_default=True,
    ),
    "pkg": dict(
        name="Package",
        name_pluralized="Packages",
        abbreviation="pkg",
        unit_type=UnitType.PIECES,
        base_factor="1.00",
        is_base_unit=False,
    ),
    "clove": dict(
        name="Clove",
        name_pluralized="Cloves",
        abbreviation="clove",
        unit_type=UnitType.PIECES,
        base_factor="0.10",
        is_base_unit=False,
    ),
    "tab": dict(
        name="Tablet",
        name_pluralized="Tablets",
        abbreviation="tab",
        unit_type=UnitType.PIECES,
        base_factor="1.00",
        is_base_unit=False,
    ),
    "par": dict(
        name="Par",
        name_pluralized=None,
        abbreviation="par",
        unit_type=UnitType.PIECES,
        base_factor="1.00",
        is_base_unit=False,
    ),
    "portion": dict(
        name="Portion",
        name_pluralized="Portions",
        abbreviation="Portions",
        unit_type=UnitType.PIECES,
        base_factor="1.00",
        is_base_unit=False,
    ),
    "stem": dict(
        name="Stem",
        name_pluralized="Stems",
        abbreviation="stem",
        unit_type=UnitType.PIECES,
        base_factor="0.10",
        is_base_unit=False,
    ),
    # Weight
    "g": dict(
        name="Gram",
        name_pluralized=None,
        abbreviation="g",
        unit_type=UnitType.WEIGHT,
        base_factor="1.00",
        is_base_unit=True,
    ),
    "kg": dict(
        name="Kilogram",
        name_pluralized=None,
        abbreviation="kg",
        unit_type=UnitType.WEIGHT,
        base_factor="1000.00",
        is_base_unit=False,
    ),
    "tsp": dict(
        name="Teaspoon",
        name_pluralized="Teaspoons",
        abbreviation="tsp",
        unit_type=UnitType.WEIGHT,
        base_factor="5.00",
        is_base_unit=False,
    ),
    "tbsp": dict(
        name="Tablespoon",
        name_pluralized="Tablespoons",
        abbreviation="tbsp",
        unit_type=UnitType.WEIGHT,
        base_factor="15.00",
        is_base_unit=False,
    ),
    "pinch": dict(
        name="Pinch",
        name_pluralized="Pinches",
        abbreviation="pinch",
        unit_type=UnitType.WEIGHT,
        base_factor="5.00",
        is_base_unit=False,
    ),
    "handful": dict(
        name="Handful",
        name_pluralized="Handfuls",
        abbreviation="handful",
        unit_type=UnitType.WEIGHT,
        base_factor="30.00",
        is_base_unit=False,
    ),
    "slice": dict(
        name="Slice",
        name_pluralized="Slices",
        abbreviation="slice",
        unit_type=UnitType.WEIGHT,
        base_factor="50.00",
        is_base_unit=False,
    ),
    # Volume
    "ml": dict(
        name="Milliliter",
        name_pluralized=None,
        abbreviation="ml",
        unit_type=UnitType.VOLUME,
        base_factor="1.00",
        is_base_unit=True,
    ),
    "l": dict(
        name="Liter",
        name_pluralized=None,
        abbreviation="l",
        unit_type=UnitType.VOLUME,
        base_factor="1000.00",
        is_base_unit=False,
    ),
    "dl": dict(
        name="Deciliter",
        name_pluralized=None,
        abbreviation="dl",
        unit_type=UnitType.VOLUME,
        base_factor="100.00",
        is_base_unit=False,
    ),
    "cl": dict(
        name="Centiliter",
        name_pluralized=None,
        abbreviation="cl",
        unit_type=UnitType.VOLUME,
        base_factor="10.00",
        is_base_unit=False,
    ),
    # Length
    "mm": dict(
        name="Millimeter",
        name_pluralized=None,
        abbreviation="mm",
        unit_type=UnitType.LENGTH,
        base_factor="1.00",
        is_base_unit=True,
    ),
    "cm": dict(
        name="Centimeter",
        name_pluralized=None,
        abbreviation="cm",
        unit_type=UnitType.LENGTH,
        base_factor="10.00",
        is_base_unit=False,
    ),
    "dm": dict(
        name="Decimeter",
        name_pluralized=None,
        abbreviation="dm",
        unit_type=UnitType.LENGTH,
        base_factor="100.00",
        is_base_unit=False,
    ),
    "m": dict(
        name="Meter",
        name_pluralized=None,
        abbreviation="m",
        unit_type=UnitType.LENGTH,
        base_factor="1000.00",
        is_base_unit=False,
    ),
    "100 m": dict(
        name="100 meter",
        name_pluralized=None,
        abbreviation="100 m",
        unit_type=UnitType.LENGTH,
        base_factor="100000.00",
        is_base_unit=False,
    ),
    # Usage
    "usage": dict(
        name="Usage",
        name_pluralized=None,
        abbreviation="usage",
        unit_type=UnitType.USAGE,
        base_factor="1.00",
        is_base_unit=True,
    ),
    "wash": dict(
        name="Wash",
        name_pluralized=None,
        abbreviation="wash",
        unit_type=UnitType.USAGE,
        base_factor="1.00",
        is_base_unit=False,
    ),
    "treatment": dict(
        name="Treatment",
        name_pluralized="Treatments",
        abbreviation="treatment",
        unit_type=UnitType.USAGE,
        base_factor="1.00",
        is_base_unit=False,
    ),
}


@pytest.fixture
def get_unit(db: Any) -> Callable[[str], Unit]:
    units: dict[str, Unit] = {}

    def _get_unit(abbreviation: str) -> Unit:
        if abbreviation in units:
            return units[abbreviation]

        assert abbreviation in UNITS
        unit, _created = Unit.objects.get_or_create(**UNITS[abbreviation])
        units[abbreviation] = unit
        return unit

    return _get_unit
