from nest.core.exceptions import ApplicationError

from .models import Unit
from .records import UnitRecord


def get_unit(pk: int | str) -> UnitRecord:
    """
    Get a unit based in id.
    """

    unit = Unit.objects.filter(id=pk).first()

    if not unit:
        raise ApplicationError(message="Unit does not exist.")

    return UnitRecord.from_unit(unit)


def get_units() -> list[UnitRecord]:
    """
    Get a list of all units.
    """
    units = Unit.objects.all()

    return [UnitRecord.from_unit(unit) for unit in units]


def get_unit_by_abbreviation(*, abbreviation: str) -> UnitRecord:
    """
    Get a unit based on its abbreviation.
    """

    unit = Unit.objects.filter(abbreviation=abbreviation).first()

    if not unit:
        raise ApplicationError(message="Unit does not exist.")

    return UnitRecord.from_unit(unit)
