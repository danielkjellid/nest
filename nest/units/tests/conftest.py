import pytest
from ..models import Unit
from ..records import UnitRecord
from .utils import create_units


@pytest.fixture
def unit_records_by_abbreviation() -> dict[str, UnitRecord]:
    if Unit.objects.count() == 0:
        create_units()

    units = Unit.objects.all()
    return {unit.abbreviation: UnitRecord.from_unit(unit) for unit in units}
