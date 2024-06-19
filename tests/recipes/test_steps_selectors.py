import pytest

from nest.recipes.steps.selectors import get_step_ingredient_items_for_steps


@pytest.mark.products(
    product1={"name": "product1"},
    product2={"name": "product2"},
    product3={"name": "product3"},
)
@pytest.mark.recipe_ingredients(
    ingredient1={"title": "Ingredient 1", "product": "product1"},
    ingredient2={"title": "Ingredient 2", "product": "product2"},
    ingredient3={"title": "Ingredient 3", "product": "product3"},
)
@pytest.mark.recipe_ingredient_item_groups(
    group1={"title": "Group 1"},
    group2={"title": "Group 2"},
)
@pytest.mark.recipe_ingredient_items(
    item1={"ingredient_group": "group1", "ingredient": "ingredient1"},
    item2={"ingredient_group": "group1", "ingredient": "ingredient2"},
    item3={"ingredient_group": "group2", "ingredient": "ingredient3"},
)
@pytest.mark.recipe_steps(
    step1={"number": 1},
    step2={"number": 2},
    step3={"number": 3},
    step4={"number": 4},
)
@pytest.mark.recipe_step_ingredient_items(
    step_item1={"step": "step1", "ingredient_item": "item1"},
    step_item2={"step": "step1", "ingredient_item": "item2"},
    step_item3={"step": "step2", "ingredient_item": "item1"},
    step_item4={"step": "step4", "ingredient_item": "item3"},
)
def test_selector_get_step_ingredient_items_for_steps(
    recipe_steps, recipe_step_ingredient_items, django_assert_num_queries
):
    """
    Test that the get_step_ingredient_items_for_steps selector correctly retrieves
    result within query limits.
    """
    step_ids = [step.id for step in recipe_steps.values()]

    with django_assert_num_queries(1):
        step_items = get_step_ingredient_items_for_steps(step_ids=step_ids)

    assert len(step_items.keys()) == len(step_ids)
    assert len(step_items[recipe_steps["step1"].id]) == 2
    assert len(step_items[recipe_steps["step2"].id]) == 1
    assert len(step_items[recipe_steps["step3"].id]) == 0
    assert len(step_items[recipe_steps["step4"].id]) == 1
