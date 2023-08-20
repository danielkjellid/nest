import pytest
from ..selectors import get_ingredient_item_groups_for_recipe
from .utils import create_recipe_ingredient_item_group, create_recipe
from ..records import RecipeIngredientItemGroupRecord

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
