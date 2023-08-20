import pytest

pytestmark = pytest.mark.django_db


class TestRecipeSelectors:
    def test_selector_get_ingredient_group_items_for_recipe(
        self, django_assert_num_queries
    ):
        assert False

    def test_selector_get_recipes(self, django_assert_num_queries):
        assert False
