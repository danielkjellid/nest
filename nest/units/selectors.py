from nest.core.exceptions import ApplicationError
from django.db.models import Value, F, CharField
from django.db.models.functions import Concat

from .models import Unit
from .records import UnitRecord


class UnitSelector:
    def __init__(self) -> None:
        ...

    @classmethod
    def get_units(cls) -> list[UnitRecord]:
        units = Unit.objects.all().annotate(
            display_name=Concat("name", Value(" ("), "abbreviation", Value(")"))
        )

        return [UnitRecord.from_unit(unit) for unit in units]

    @classmethod
    def get_unit_from_abbreviation(cls, abbreviation: str) -> UnitRecord:
        """
        Get a unit based on its abbreviation.
        """

        unit = Unit.objects.filter(abbreviation=abbreviation).first()

        if not unit:
            raise ApplicationError(message="Unit does not exist.")

        return UnitRecord.from_unit(unit)
