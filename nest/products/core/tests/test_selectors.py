import pytest

from nest.products.core.selectors import (
    get_products,
)
from nest.products.core.tests.utils import create_product

pytestmark = pytest.mark.django_db


class TestProductsSelectors:
    def test_all_products(self, django_assert_num_queries):
        """
        Test that the all_products selector returns expected output within
        query limits.
        """
        create_product(name="Test product 1")
        create_product(name="Test product 2")
        create_product(name="Test product 3")

        with django_assert_num_queries(1):
            products = get_products()

        assert len(products) == 3
