from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

from nest.recipes.core.enums import RecipeStatus
from nest.recipes.plans.selectors import find_recipes_applicable_for_plan

_FREEZE_TIME = datetime(year=2024, month=1, day=8, hour=12, minute=0, second=0)
_GRACE_PERIOD = timedelta(weeks=2)


@freeze_time(_FREEZE_TIME)
@pytest.mark.recipes(
    recipe1={"title": "Recipe 1", "status": RecipeStatus.PUBLISHED},
    recipe2={"title": "Recipe 2", "status": RecipeStatus.DRAFT},
    recipe3={"title": "Recipe 3", "status": RecipeStatus.PUBLISHED},
)
@pytest.mark.recipe_plans(
    plan1={"title": "Plan 1", "from_date": _FREEZE_TIME - _GRACE_PERIOD}
)
@pytest.mark.recipe_plan_item(recipe_plan="plan1", recipe="recipe3")
def test_selector_find_recipes_applicable_for_plan(
    recipes, recipe_plans, recipe_plan_item, django_assert_num_queries
):
    with django_assert_num_queries(3):
        applicable_recipes = find_recipes_applicable_for_plan(grace_period_weeks=1)

    recipe_ids = [recipe.id for recipe in applicable_recipes]

    assert recipes["recipe1"].id in recipe_ids
    assert recipes["recipe3"].id not in recipe_ids
    assert recipes["recipe2"].id not in recipe_ids
