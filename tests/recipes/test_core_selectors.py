import pytest

from nest.core.exceptions import ApplicationError
from nest.recipes.core.models import Recipe
from nest.recipes.core.selectors import get_recipe, get_recipe_data
from tests.helpers.types import AnyOrder


@pytest.mark.recipes(recipe1={"title": "Recipe 1"})
@pytest.mark.parametrize("return_value", ("recipe1", None))
def test_selector_get_recipe(mocker, recipes, return_value):
    recipe = recipes["recipe1"]
    returns = recipe if return_value is not None else None

    get_recipes_mock = mocker.patch(
        "nest.recipes.core.selectors.get_recipes_by_id",
        return_value={recipe.id: returns},
    )

    if return_value is None:
        with pytest.raises(ApplicationError):
            get_recipe(pk=recipe.id)
    else:
        assert get_recipe(pk=recipe.id).id == recipe.id

    get_recipes_mock.assert_called_once_with(recipe_ids=[recipe.id])


@pytest.mark.recipes(
    recipe1={"title": "Recipe 1"},
    recipe2={"title": "Recipe 2"},
    recipe3={"title": "Recipe 3"},
)
def test_selector_get_recipe_data(django_assert_num_queries, recipes, mocker):
    recipe1 = recipes["recipe1"]
    recipe2 = recipes["recipe2"]
    recipe3 = recipes["recipe3"]

    steps_mock = mocker.patch(
        "nest.recipes.core.selectors.get_steps_for_recipes",
        return_value={
            recipe1.id: [],
            recipe2.id: [],
            recipe3.id: [],
        },
    )
    ingredient_groups_mock = mocker.patch(
        "nest.recipes.core.selectors.get_recipe_ingredient_item_groups_for_recipes",
        return_value={
            recipe1.id: [],
            recipe2.id: [],
            recipe3.id: [],
        },
    )

    with django_assert_num_queries(1):
        fetched_recipes = get_recipe_data(qs=Recipe.objects.all())

    assert len(fetched_recipes.values()) == 3
    steps_mock.assert_called_once_with(
        recipe_ids=AnyOrder([recipe1.id, recipe2.id, recipe3.id])
    )
    ingredient_groups_mock.assert_called_once_with(
        recipe_ids=AnyOrder([recipe1.id, recipe2.id, recipe3.id])
    )
