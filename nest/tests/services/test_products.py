import pytest

pytestmark = pytest.mark.django_db


class TestProductService:
    def test_update_or_create_product(self, django_assert_num_queries):
        assert False

    def test_import_from_oda(self, django_assert_num_queries):
        assert False
