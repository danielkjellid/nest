import pytest
from nest.core.exceptions import ApplicationError

from ..records import RecipeRecord
from .utils import create_recipe

from ..selectors import get_recipe, get_recipes

pytestmark = pytest.mark.django_db


class TestRecipeCoreSelectors:
    def test_selector_get_recipe(self, django_assert_num_queries, mocker):
        """
        Test that the get_recipe selector retrieves a recipe within query limits. Note:
        This selector does more than one query, but it calls other selectors which are
        tested in isolation, therefore, we just make sure they are called here.
        """
        recipe = create_recipe()
        steps_selector_mock = mocker.patch(
            "nest.recipes.core.selectors.get_steps_for_recipe", return_value=[]
        )
        ingredient_groups_selector_mock = mocker.patch(
            "nest.recipes.core.selectors.get_recipe_ingredient_item_groups_for_recipe",
            return_value=[],
        )

        with django_assert_num_queries(1):
            fetched_recipe = get_recipe(pk=recipe.id)

        steps_selector_mock.assert_called_once_with(recipe_id=recipe.id)
        ingredient_groups_selector_mock.assert_called_once_with(recipe_id=recipe.id)

        assert fetched_recipe.id == recipe.id

        with pytest.raises(ApplicationError):
            get_recipe(pk=9999)

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
