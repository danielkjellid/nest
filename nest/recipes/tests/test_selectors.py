import pytest

from ..records import RecipeIngredientItemGroupRecord, RecipeRecord
from ..selectors import get_ingredient_item_groups_for_recipe, get_recipes
from .utils import create_recipe, create_recipe_ingredient_item_group

pytestmark = pytest.mark.django_db


class TestRecipeSelectors:
    def test_selector_get_ingredient_item_groups_for_recipe(
        self, django_assert_num_queries
    ):
        """
        Test that the get_ingredient_item_groups_for_recipe selector returns expected
        output within query limits.
        """
        recipe = create_recipe()
        group1 = create_recipe_ingredient_item_group(
            recipe=recipe, ordering=1, title="Group 1"
        )
        create_recipe_ingredient_item_group(recipe=recipe, ordering=2, title="Group 2")
        create_recipe_ingredient_item_group(recipe=recipe, ordering=3, title="Group 3")
        create_recipe_ingredient_item_group(recipe=recipe, ordering=4, title="Group 4")

        with django_assert_num_queries(2):
            ingredient_item_groups = get_ingredient_item_groups_for_recipe(
                recipe_id=recipe.id
            )

        assert len(ingredient_item_groups) == 4
        assert ingredient_item_groups[0] == RecipeIngredientItemGroupRecord.from_group(
            group1, skip_check=True
        )

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
