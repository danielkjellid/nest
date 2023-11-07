from decimal import ROUND_HALF_UP, Decimal

from nest.core.exceptions import ApplicationError

from .enums import UnitType
from .models import Unit
from .records import UnitRecord
from .utils import convert_unit_quantity


def get_units() -> list[UnitRecord]:
    """
    Get a list of all units.
    """
    units = Unit.objects.all()

    return [UnitRecord.from_unit(unit) for unit in units]


def get_unit_by_abbreviation(abbreviation: str) -> UnitRecord:
    """
    Get a unit based on its abbreviation.
    """

    unit = Unit.objects.filter(abbreviation=abbreviation).first()

    if not unit:
        raise ApplicationError(message="Unit does not exist.")

    return UnitRecord.from_unit(unit)


def get_unit_normalized_quantity(
    *, quantity: Decimal, unit: UnitRecord
) -> tuple[Decimal, UnitRecord]:
    """
    Get the normalized quantity based on a given unit. Depdending on the quantity, we'll
    convert the value to the highest or lowest possible unit in the same hierarchy.


    """
    if quantity < Decimal("1.00"):
        return get_unit_lowest_normalized_quantity(quantity=quantity, unit=unit)
    else:
        return get_unit_highest_normalized_quantity(quantity=quantity, unit=unit)


def get_unit_lowest_normalized_quantity(
    *, quantity: Decimal, unit: UnitRecord
) -> tuple[Decimal, UnitRecord]:
    """
    Try to normalize quantity by using the lowest unit in the same hierarchy as the
    given the unit.
    """
    if unit.unit_type == UnitType.WEIGHT:
        to_unit = get_unit_by_abbreviation(abbreviation="g")
    elif unit.unit_type == UnitType.VOLUME:
        to_unit = get_unit_by_abbreviation(abbreviation="ml")
    elif unit.unit_type == UnitType.LENGTH:
        to_unit = get_unit_by_abbreviation(abbreviation="cm")
    else:
        return quantity, unit

    return convert_unit_quantity(quantity=quantity, from_unit=unit, to_unit=to_unit)


def get_unit_highest_normalized_quantity(
    *, quantity: Decimal, unit: UnitRecord
) -> tuple[Decimal, UnitRecord]:
    """
    Try to normalize quantity by using the highest unit in the same hierarchy as the
    given the unit.
    """

    if unit.unit_type == UnitType.WEIGHT:
        to_unit = get_unit_by_abbreviation(abbreviation="kg")
    elif unit.unit_type == UnitType.VOLUME:
        to_unit = get_unit_by_abbreviation(abbreviation="l")
    elif unit.unit_type == UnitType.LENGTH:
        to_unit = get_unit_by_abbreviation(abbreviation="m")
    else:
        return quantity, unit

    return convert_unit_quantity(quantity=quantity, from_unit=unit, to_unit=to_unit)


def get_unit_normalized_price(
    *, price: Decimal, quantity: Decimal, unit: Unit
) -> tuple[Decimal, UnitRecord]:
    """
    Given the price un a unit, convert this to the normal unit in that group for that
    quantity. E.g. weight units are normalized to kg to get price per kg.
    """

    converted_quantity, normalized_unit = get_unit_highest_normalized_quantity(
        quantity=quantity, unit=unit
    )

    # Calculate and round price.
    unit_price = Decimal(price / converted_quantity)
    unit_price = unit_price.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

    return unit_price, normalized_unit
