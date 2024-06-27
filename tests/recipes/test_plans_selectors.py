from datetime import datetime, timedelta

import pytest
from django.utils.timezone import make_aware
from freezegun import freeze_time

from nest.recipes.core.enums import RecipeStatus
from nest.recipes.plans.selectors import (
    find_recipes_applicable_for_plan,
    get_recipe_plan_items_for_plans,
    get_recipe_plans_for_home,
)
from tests.factories.records import RecipeDetailRecordFactory
from tests.helpers.types import AnyOrder

_FREEZE_TIME = make_aware(
    datetime(year=2024, month=1, day=8, hour=12, minute=0, second=0)
)
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


@pytest.mark.recipe_plans(plan1={"title": "Plan 1"}, plan2={"title": "Plan 2"})
@pytest.mark.recipes(
    recipe1={"title": "Recipe 1"},
    recipe2={"title": "Recipe 2"},
    recipe3={"title": "Recipe 3"},
)
@pytest.mark.recipe_plan_items(
    plan_item1={"recipe_plan": "plan1", "recipe": "recipe1"},
    plan_item2={"recipe_plan": "plan1", "recipe": "recipe2"},
    plan_item3={"recipe_plan": "plan2", "recipe": "recipe3"},
)
def test_selector_get_recipe_plan_items_for_plan(
    django_assert_num_queries, recipe_plans, recipe_plan_items, mocker, recipes
):
    plan1 = recipe_plans["plan1"]
    plan2 = recipe_plans["plan2"]

    recipe1 = recipes["recipe1"]
    recipe2 = recipes["recipe2"]
    recipe3 = recipes["recipe3"]

    recipes_mock = mocker.patch(
        "nest.recipes.plans.selectors.get_recipes_by_id",
        return_value={
            recipe1.id: RecipeDetailRecordFactory.build(),
            recipe2.id: RecipeDetailRecordFactory.build(),
            recipe3.id: RecipeDetailRecordFactory.build(),
        },
    )

    plan_item1 = recipe_plan_items["plan_item1"]
    plan_item2 = recipe_plan_items["plan_item2"]
    plan_item3 = recipe_plan_items["plan_item3"]

    with django_assert_num_queries(1):
        items = get_recipe_plan_items_for_plans(plan_ids=[plan1.id, plan2.id])

    assert {i.id for i in items[plan1.id]} == {plan_item1.id, plan_item2.id}
    assert {i.id for i in items[plan2.id]} == {plan_item3.id}

    recipes_mock.assert_called_once_with(
        recipe_ids=AnyOrder([recipe.id for recipe in recipes.values()])
    )


@pytest.mark.homes(
    home1={"street_address": "Example street"},
    home2={"street_address": "Example citystreet"},
)
@pytest.mark.recipe_plans(
    plan1={"title": "Plan 1", "home": "home1"},
    plan2={"title": "Plan 2", "home": "home2"},
    plan3={"title": "Plan 3", "home": "home1"},
)
def test_selector_get_recipe_plans_for_home(
    django_assert_num_queries, homes, recipe_plans, mocker
):
    home1 = homes["home1"]

    plan1 = recipe_plans["plan1"]
    plan2 = recipe_plans["plan2"]
    plan3 = recipe_plans["plan3"]

    plan_items_mock = mocker.patch(
        "nest.recipes.plans.selectors.get_recipe_plan_items_for_plans",
        return_value={
            plan1.id: [],
            plan2.id: [],
            plan3.id: [],
        },
    )

    with django_assert_num_queries(1):
        fetched_plans = get_recipe_plans_for_home(home_id=home1)

    assert {plan.id for plan in fetched_plans} == {plan1.id, plan3.id}
    plan_items_mock.assert_called_once_with(plan_ids=AnyOrder([plan1.id, plan3.id]))
