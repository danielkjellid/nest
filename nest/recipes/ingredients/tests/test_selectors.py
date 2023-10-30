import pytest
from django.db.models import Q

from nest.products.tests.utils import create_product
from nest.recipes.core.tests.utils import create_recipe
from nest.recipes.steps.tests.utils import create_recipe_step

from ..selectors import (
    _get_recipe_ingredient_items,
    get_recipe_ingredient_item_groups_for_recipes,
    get_recipe_ingredient_items_for_groups,
    get_recipe_ingredient_items_for_steps,
    get_recipe_ingredients,
)
from .utils import (
    create_recipe_ingredient,
    create_recipe_ingredient_item,
    create_recipe_ingredient_item_group,
)

pytestmark = pytest.mark.django_db


class TestRecipeIngredientsSelectors:
    def test_selector__get_recipe_ingredient_items(self, django_assert_num_queries):
        """
        Test that the _get_ingredient_items selector operates within query limits and
        outputs correctly.
        """
        recipe1 = create_recipe(title="Recipe 1")
        create_recipe_ingredient_item(
            ingredient_group=create_recipe_ingredient_item_group(
                title="Group 1", recipe=recipe1
            ),
            step=create_recipe_step(
                recipe=recipe1, number=1, instruction="Some instruction"
            ),
            ingredient=create_recipe_ingredient(
                title="Tomatoes, red", product=create_product(name="Red tomatoes")
            ),
        )
        recipe2 = create_recipe(title="Recipe 2")
        create_recipe_ingredient_item(
            ingredient_group=create_recipe_ingredient_item_group(
                title="Group 2", recipe=recipe2
            ),
            step=create_recipe_step(
                recipe=recipe2, number=1, instruction="Some instruction"
            ),
            ingredient=create_recipe_ingredient(
                title="Sausage", product=create_product(name="Italian sausage")
            ),
        )

        with django_assert_num_queries(5):
            ingredient_items = _get_recipe_ingredient_items()

        assert len(ingredient_items) == 2

    def test_selector_get_recipe_ingredient_items_for_groups(self, mocker):
        """
        Make sure that the get_ingredient_items_for_groups selector calls the
        _get_ingredient_items selector with correct filter expression.
        """

        group_ids = [1, 2, 3]
        selector_mock = mocker.patch(
            "nest.recipes.ingredients.selectors._get_recipe_ingredient_items"
        )
        ingredient_items = get_recipe_ingredient_items_for_groups(group_ids=group_ids)

        selector_mock.assert_called_once_with(Q(ingredient_group_id__in=group_ids))

        assert len(ingredient_items.keys()) == 3
        assert all(key in group_ids for key in ingredient_items.keys())

    def test_selector_get_ingredient_items_for_steps(self, mocker):
        """
        Make sure that the get_ingredient_items_for_steps selector calls the
        _get_ingredient_items selector with correct filter expression.
        """

        step_ids = [4, 5, 6, 7]
        selector_mock = mocker.patch(
            "nest.recipes.ingredients.selectors._get_ingredient_items"
        )
        ingredient_items = get_recipe_ingredient_items_for_steps(step_ids=step_ids)

        selector_mock.assert_called_once_with(Q(step_id__in=step_ids))

        assert len(ingredient_items.keys()) == 4
        assert all(key in step_ids for key in ingredient_items.keys())

    def test_selector_get_ingredient_item_groups_for_recipes(
        self, django_assert_num_queries
    ):
        """
        Test that given a list of recipes, we're able to retrieve the correct ingredient
        item groups related to each respective recipe within query limits.
        """
        recipe1 = create_recipe(title="Recipe 1")
        recipe1_ingredient_item_group = create_recipe_ingredient_item_group(
            title="Group 1", recipe=recipe1
        )
        create_recipe_ingredient_item(
            ingredient_group=recipe1_ingredient_item_group,
            step=create_recipe_step(
                recipe=recipe1, number=1, instruction="Some instruction"
            ),
            ingredient=create_recipe_ingredient(
                title="Tomatoes, red", product=create_product(name="Red tomatoes")
            ),
        )
        recipe2 = create_recipe(title="Recipe 2")
        recipe2_ingredient_item_group1 = create_recipe_ingredient_item_group(
            title="Group 2", recipe=recipe2, ordering=1
        )
        create_recipe_ingredient_item(
            ingredient_group=recipe2_ingredient_item_group1,
            step=create_recipe_step(
                recipe=recipe2, number=1, instruction="Some instruction"
            ),
            ingredient=create_recipe_ingredient(
                title="Sausage", product=create_product(name="Italian sausage")
            ),
        )
        recipe2_ingredient_item_group2 = create_recipe_ingredient_item_group(
            title="Group 2", recipe=recipe2, ordering=2
        )
        create_recipe_ingredient_item(
            ingredient_group=recipe2_ingredient_item_group2,
            step=create_recipe_step(
                recipe=recipe2, number=2, instruction="Some instruction"
            ),
            ingredient=create_recipe_ingredient(
                title="Bacon", product=create_product(name="Bacon")
            ),
        )

        with django_assert_num_queries(6):
            ingredient_item_groups = get_recipe_ingredient_item_groups_for_recipes(
                recipe_ids=[recipe1.id, recipe2.id]
            )

        assert (
            ingredient_item_groups[recipe1.id][0].id == recipe1_ingredient_item_group.id
        )
        assert (
            ingredient_item_groups[recipe2.id][0].id
            == recipe2_ingredient_item_group1.id
        )
        assert (
            ingredient_item_groups[recipe2.id][1].id
            == recipe2_ingredient_item_group2.id
        )

    def test_selector_get_recipe_ingredients(self, django_assert_num_queries):
        """
        Test that the get_ingredients selector returns expected output within
        query limits.
        """

        create_recipe_ingredient(
            title="Ingredient 1", product=create_product(name="Product 1")
        )
        create_recipe_ingredient(
            title="Ingredient 2", product=create_product(name="Product 2")
        )
        create_recipe_ingredient(
            title="Ingredient 3", product=create_product(name="Product 3")
        )

        with django_assert_num_queries(1):
            ingredients = get_recipe_ingredients()

        assert len(ingredients) == 3
