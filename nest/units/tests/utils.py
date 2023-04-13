from nest.units.enums import UnitType
from nest.units.models import Unit

units = [
    Unit(
        name="Stykk",
        name_pluralized="Stykker",
        abbreviation="stk",
        unit_type=UnitType.PIECES,
        base_factor="1.00",
        is_base_unit=True,
        is_default=True,
    ),
    Unit(
        name="Pakke",
        name_pluralized="Pakker",
        abbreviation="pk",
        unit_type=UnitType.PIECES,
        base_factor="1.00",
        is_base_unit=False,
    ),
    Unit(
        name="Porsjon",
        abbreviation="prosjon",
        unit_type=UnitType.PIECES,
        base_factor="1.00",
        is_base_unit=False,
    ),
    # Weight
    Unit(
        name="Gram",
        abbreviation="g",
        unit_type=UnitType.WEIGHT,
        base_factor="1.00",
        is_base_unit=True,
    ),
    Unit(
        name="Kilogram",
        abbreviation="kg",
        unit_type=UnitType.WEIGHT,
        base_factor="1000.00",
        is_base_unit=False,
    ),
    # Volume
    Unit(
        name="Milliliter",
        abbreviation="ml",
        unit_type=UnitType.WEIGHT,
        base_factor="1.00",
        is_base_unit=True,
    ),
    Unit(
        name="Liter",
        abbreviation="l",
        unit_type=UnitType.WEIGHT,
        base_factor="1000.00",
        is_base_unit=False,
    ),
    Unit(
        name="Desiliter",
        abbreviation="dl",
        unit_type=UnitType.VOLUME,
        base_factor="100.00",
        is_base_unit=False,
    ),
    Unit(
        name="Centiliter",
        abbreviation="cl",
        unit_type=UnitType.VOLUME,
        base_factor="10.00",
        is_base_unit=False,
    ),
    # Length
    Unit(
        name="Millimeter",
        abbreviation="mm",
        unit_type=UnitType.LENGTH,
        base_factor="1.00",
        is_base_unit=True,
    ),
    Unit(
        name="Centimeter",
        abbreviation="cm",
        unit_type=UnitType.LENGTH,
        base_factor="10.00",
        is_base_unit=False,
    ),
    Unit(
        name="Desimeter",
        abbreviation="dm",
        unit_type=UnitType.LENGTH,
        base_factor="100.00",
        is_base_unit=False,
    ),
    Unit(
        name="Meter",
        abbreviation="m",
        unit_type=UnitType.LENGTH,
        base_factor="1000.00",
        is_base_unit=False,
    ),
]


def create_units() -> None:
    Unit.objects.bulk_create(units, ignore_conflicts=True)


def get_unit(abbreviation: str = "kg") -> Unit:
    if Unit.objects.all().count() == 0:
        create_units()

    return Unit.objects.get(abbreviation=abbreviation)
