import pytest
from nest.tests.utilities import create_units
from nest.selectors import UnitSelector
from nest.exceptions import ApplicationError

pytestmark = pytest.mark.django_db


class TestUnitSelector:
    def test_get_unit_from_abbreviation(self, django_assert_num_queries):
        """
        Test that the get_unit_from_abbreviation correctly retrieves the right unit,
        withing query limits, as well as raises ApplicationError if unit does not exist.
        """
        create_units()

        with django_assert_num_queries(1):
            kg = UnitSelector.get_unit_from_abbreviation(abbreviation="kg")

        assert kg is not None
        assert kg.abbreviation == "kg"

        with django_assert_num_queries(1):
            g = UnitSelector.get_unit_from_abbreviation(abbreviation="g")

        assert g is not None
        assert g.abbreviation == "g"

        with pytest.raises(ApplicationError):
            UnitSelector.get_unit_from_abbreviation(abbreviation="doesnotexist")
