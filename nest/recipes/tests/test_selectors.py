import pytest
from django.db.models import Q

from nest.core.exceptions import ApplicationError
from nest.ingredients.tests.utils import create_ingredient
from nest.products.tests.utils import create_product

from ..records import RecipeRecord
from ..selectors import (
    _get_ingredient_items,
    get_ingredient_item_groups_for_recipes,
    get_ingredient_items_for_groups,
    get_ingredient_items_for_steps,
    get_recipe,
    get_recipes,
    get_steps_for_recipes,
)
from .utils import (
    create_recipe,
    create_recipe_ingredient_item,
    create_recipe_ingredient_item_group,
    create_recipe_step,
)

pytestmark = pytest.mark.django_db


class TestRecipeSelectors:
    def test_selector__get_ingredient_items(self, django_assert_num_queries):
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
            ingredient=create_ingredient(
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
            ingredient=create_ingredient(
                title="Sausage", product=create_product(name="Italian sausage")
            ),
        )

        with django_assert_num_queries(5):
            ingredient_items = _get_ingredient_items()

        assert len(ingredient_items) == 2

    def test_selector_get_ingredient_items_for_groups(self, mocker):
        """
        Make sure that the get_ingredient_items_for_groups selector calls the
        _get_ingredient_items selector with correct filter expression.
        """

        group_ids = [1, 2, 3]
        selector_mock = mocker.patch("nest.recipes.selectors._get_ingredient_items")
        ingredient_items = get_ingredient_items_for_groups(group_ids=group_ids)

        selector_mock.assert_called_once_with(Q(ingredient_group_id__in=group_ids))

        assert len(ingredient_items.keys()) == 3
        assert all(key in group_ids for key in ingredient_items.keys())

    def test_selector_get_ingredient_items_for_steps(self, mocker):
        """
        Make sure that the get_ingredient_items_for_steps selector calls the
        _get_ingredient_items selector with correct filter expression.
        """

        step_ids = [4, 5, 6, 7]
        selector_mock = mocker.patch("nest.recipes.selectors._get_ingredient_items")
        ingredient_items = get_ingredient_items_for_steps(step_ids=step_ids)

        selector_mock.assert_called_once_with(Q(step_id__in=step_ids))

        assert len(ingredient_items.keys()) == 4
        assert all(key in step_ids for key in ingredient_items.keys())

    def test_selector_get_ingredient_item_groups_for_recipe(
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
            ingredient=create_ingredient(
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
            ingredient=create_ingredient(
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
            ingredient=create_ingredient(
                title="Bacon", product=create_product(name="Bacon")
            ),
        )

        with django_assert_num_queries(6):
            ingredient_item_groups = get_ingredient_item_groups_for_recipes(
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
            ingredient=create_ingredient(
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
            ingredient=create_ingredient(
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
            ingredient=create_ingredient(
                title="Bacon", product=create_product(name="Bacon")
            ),
        )

        with django_assert_num_queries(6):
            steps = get_steps_for_recipes(recipe_ids=[recipe1.id, recipe2.id])

        assert steps[recipe1.id][0].id == recipe1_step.id
        assert steps[recipe2.id][0].id == recipe2_step1.id
        assert steps[recipe2.id][1].id == recipe2_step2.id

    def test_selector_get_recipe(self, django_assert_num_queries, mocker):
        """
        Test that the get_recipe selector retrieves a recipe within query limits. Note:
        This selector does more than one query, but it calls other selectors which are
        tested in isolation, therefore, we just make sure they are called here.
        """
        recipe = create_recipe()
        steps_selector_mock = mocker.patch(
            "nest.recipes.selectors.get_steps_for_recipe", return_value=[]
        )
        ingredient_groups_selector_mock = mocker.patch(
            "nest.recipes.selectors.get_ingredient_item_groups_for_recipe",
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
