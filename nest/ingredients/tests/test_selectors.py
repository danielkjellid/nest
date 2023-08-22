import pytest

from nest.products.tests.utils import create_product

from ..selectors import get_ingredients
from .utils import create_ingredient

pytestmark = pytest.mark.django_db


class TestIngredientsSelectors:
    def test_selector_get_ingredients(self, django_assert_num_queries):
        """
        Test that the get_ingredients selector returns expected output within
        query limits.
        """

        create_ingredient(
            title="Ingredient 1", product=create_product(name="Product 1")
        )
        create_ingredient(
            title="Ingredient 2", product=create_product(name="Product 2")
        )
        create_ingredient(
            title="Ingredient 3", product=create_product(name="Product 3")
        )

        with django_assert_num_queries(1):
            ingredients = get_ingredients()

        assert len(ingredients) == 3
