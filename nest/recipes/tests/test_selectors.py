import pytest

from ..records import RecipeIngredientItemGroupRecord, RecipeRecord
from ..selectors import get_recipe_ingredient_item_groups, get_recipes
from .utils import create_recipe, create_recipe_ingredient_item_group

pytestmark = pytest.mark.django_db


class TestRecipeSelectors:
    def test_selector__get_ingredient_items(self):
        assert False

    def test_selector_get_ingredient_items_for_groups(self):
        assert False

    def test_selector_get_ingredient_items_for_steps(self):
        assert False

    def test_selector_get_ingredient_item_groups_for_recipe(self):
        assert False

    def test_selector_get_steps_for_recipes(self):
        assert False

    def test_selector_get_recipe(self):
        assert False

    def test_selector_get_recipes(self, django_assert_num_queries):
        """
        Test that the get_recipes selector returns expected output within query limits.
        """

        recipe1 = create_recipe(title="Recipe 1")
        create_recipe(title="Recipe 2")
        create_recipe(title="Recipe 3")
        recipe4 = create_recipe(title="Recipe 4")

        with django_assert_num_queries(1):
            recipes = get_recipes()

        assert len(recipes) == 4
        assert recipes[0] == RecipeRecord.from_recipe(recipe4)
        assert recipes[3] == RecipeRecord.from_recipe(recipe1)
