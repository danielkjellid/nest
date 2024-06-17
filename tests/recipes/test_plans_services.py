from decimal import Decimal

import pytest
from django.utils import timezone

from nest.recipes.plans.algorithm import PlanDistributor
from nest.recipes.plans.models import RecipePlan, RecipePlanItem
from nest.recipes.plans.services import _create_recipe_plan_items, create_recipe_plan
from tests.factories.records import RecipeDetailRecordFactory

pytestmark = pytest.mark.django_db


def test_service_create_recipe_plan(
    django_assert_num_queries, immediate_on_commit, mocker
):
    """
    Test that the create_recipe_plan runs creates the plan instance and runs
    the required methods to create a full plan.
    """
    grace_period_weeks = 1
    budget = Decimal("100.00")
    num_items = 1
    num_pescatarian = 1
    num_vegetarian = 1
    applicable_recipes = []

    applicable_recipes_mock = mocker.patch(
        "nest.recipes.plans.services.find_recipes_applicable_for_plan",
        return_value=applicable_recipes,
    )
    create_items_mock = mocker.patch(
        "nest.recipes.plans.services._create_recipe_plan_items"
    )
    distr_mock = mocker.patch.object(PlanDistributor, "create_plan", return_value=[])

    initial_count = RecipePlan.objects.count()

    with django_assert_num_queries(3), immediate_on_commit:
        create_recipe_plan(
            title="Example title",
            description=None,
            budget=budget,
            num_portions_per_recipe=4,
            num_items=num_items,
            num_pescatarian=num_pescatarian,
            num_vegetarian=num_vegetarian,
            grace_period_weeks=grace_period_weeks,
            from_date=timezone.now(),
        )

    # Assert that a new plan is created.
    assert RecipePlan.objects.count() == initial_count + 1

    # Assert that mocks are called accordingly.
    applicable_recipes_mock.assert_called_once_with(
        grace_period_weeks=grace_period_weeks,
    )
    distr_mock.assert_called_once()
    create_items_mock.assert_called_once()


@pytest.mark.recipes(
    recipe1={"title": " Recipe 1"},
    recipe2={"title": " Recipe 2"},
    recipe3={"title": " Recipe 3"},
)
@pytest.mark.recipe_plan(title="My plan")
def test_service__create_recipe_plan_items(
    django_assert_num_queries, recipes, recipe_plan
):
    """
    Test that the _create_recipe_plan_items creates plan items associated to the correct
    recipe plan.
    """
    recipe_records = [
        RecipeDetailRecordFactory.build(id=recipe.id) for recipe in recipes.values()
    ]

    initial_count = RecipePlanItem.objects.filter(recipe_plan_id=recipe_plan.id).count()

    with django_assert_num_queries(2):
        _create_recipe_plan_items(plan_id=recipe_plan.id, recipes=recipe_records)

    assert RecipePlanItem.objects.filter(
        recipe_plan_id=recipe_plan.id
    ).count() == initial_count + len(recipe_records)
