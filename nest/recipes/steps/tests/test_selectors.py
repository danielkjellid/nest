import pytest

from nest.products.tests.utils import create_product
from nest.recipes.core.tests.utils import create_recipe
from nest.recipes.ingredients.tests.utils import (
    create_recipe_ingredient,
    create_recipe_ingredient_item,
    create_recipe_ingredient_item_group,
)

from ..selectors import get_steps_for_recipes
from .utils import create_recipe_step

pytestmark = pytest.mark.django_db


class TestRecipeStepsSelectors:
    def test_selector_get_steps_for_recipes(self, django_assert_num_queries):
        """
        Test that given a list of recipes, we're able to retrieve the correct steps
        related to each respective recipe within query limits.
        """
        recipe1 = create_recipe(title="Recipe 1")
        recipe1_step = create_recipe_step(
            recipe=recipe1, number=1, instruction="Some instruction"
        )
        create_recipe_ingredient_item(
            ingredient_group=create_recipe_ingredient_item_group(
                title="Group 1", recipe=recipe1
            ),
            step=recipe1_step,
            ingredient=create_recipe_ingredient(
                title="Tomatoes, red", product=create_product(name="Red tomatoes")
            ),
        )

        recipe2 = create_recipe(title="Recipe 2")
        recipe2_step1 = create_recipe_step(
            recipe=recipe2, number=1, instruction="Some instruction"
        )
        create_recipe_ingredient_item(
            ingredient_group=create_recipe_ingredient_item_group(
                title="Group 2", recipe=recipe2, ordering=1
            ),
            step=recipe2_step1,
            ingredient=create_recipe_ingredient(
                title="Sausage", product=create_product(name="Italian sausage")
            ),
        )

        recipe2_step2 = create_recipe_step(
            recipe=recipe2, number=1, instruction="Some instruction"
        )
        create_recipe_ingredient_item(
            ingredient_group=create_recipe_ingredient_item_group(
                title="Group 2", recipe=recipe2, ordering=1
            ),
            step=recipe2_step2,
            ingredient=create_recipe_ingredient(
                title="Bacon", product=create_product(name="Bacon")
            ),
        )

        with django_assert_num_queries(6):
            steps = get_steps_for_recipes(recipe_ids=[recipe1.id, recipe2.id])

        assert steps[recipe1.id][0].id == recipe1_step.id
        assert steps[recipe2.id][0].id == recipe2_step1.id
        assert steps[recipe2.id][1].id == recipe2_step2.id
