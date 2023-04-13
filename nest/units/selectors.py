from nest.core.exceptions import ApplicationError
from .models import Unit
from .records import UnitRecord


class UnitSelector:
    def __init__(self) -> None:
        ...

    @classmethod
    def get_unit_from_abbreviation(cls, abbreviation: str) -> UnitRecord:
        """
        Get a unit based on its abbreviation.
        """

        unit = Unit.objects.filter(abbreviation=abbreviation).first()

        if not unit:
            raise ApplicationError(message="Unit does not exist.")

        return UnitRecord.from_unit(unit)
