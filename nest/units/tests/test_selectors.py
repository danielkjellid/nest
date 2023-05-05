import pytest

from nest.core.exceptions import ApplicationError
from nest.units.selectors import get_unit_by_abbreviation, get_units
from nest.units.tests.utils import create_units

pytestmark = pytest.mark.django_db


class TestUnitSelector:
    def test_get_unit(self):
        assert False

    def test_get_units(self, django_assert_num_queries):
        """
        Test that all_units selector returns all units available within query limits.
        """
        create_units()  # 26 units.

        with django_assert_num_queries(1):
            units = get_units()

        assert len(units) == 26

    def test_get_unit_by_abbreviation(self, django_assert_num_queries):
        """
        Test that the get_unit_from_abbreviation correctly retrieves the right unit,
        withing query limits, as well as raises ApplicationError if unit does not exist.
        """
        create_units()

        with django_assert_num_queries(1):
            kg = get_unit_by_abbreviation(abbreviation="kg")

        assert kg is not None
        assert kg.abbreviation == "kg"

        with django_assert_num_queries(1):
            g = get_unit_by_abbreviation(abbreviation="g")

        assert g is not None
        assert g.abbreviation == "g"

        with pytest.raises(ApplicationError):
            get_unit_by_abbreviation(abbreviation="doesnotexist")
