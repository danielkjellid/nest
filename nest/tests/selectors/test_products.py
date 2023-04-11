import pytest

pytestmark = pytest.mark.django_db


class TestProductSelector:
    def test_get_product(self, django_assert_num_queries):
        assert False

    def test_all_products(self, django_assert_num_queries):
        assert False

    def test__get_product(self, django_assert_num_queries):
        assert False
