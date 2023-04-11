import pytest

pytestmark = pytest.mark.django_db


class TestUnitSelector:
    def test_get_unit_from_abbreviation(self, django_assert_num_queries):
        assert False
