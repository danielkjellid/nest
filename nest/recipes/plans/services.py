import functools
from datetime import date, timedelta
from decimal import Decimal

from django.db import transaction
from django.utils.text import slugify

from nest.homes.records import HomeRecord
from nest.recipes.core.records import RecipeDetailRecord
from nest.recipes.plans.algorithm import PlanDistributor
from nest.recipes.plans.models import RecipePlan, RecipePlanItem
from nest.recipes.plans.selectors import find_recipes_applicable_for_plan


def create_weekly_recipe_plan_for_home(
    *,
    home: HomeRecord,
    from_date: date,
    auto_generated: bool = False,
) -> None:
    num_items = 7
    week_number = from_date.isocalendar().week
    to_date = from_date + timedelta(days=num_items)
    title = f"Weekly plan {week_number} ({from_date} - {to_date}"
    description = (
        f"Automatically generated recipe plan for week {week_number}"
        if auto_generated
        else f"Weekly recipe plan for week {week_number}"
    )

    create_recipe_plan(
        title=title,
        description=description,
        from_date=from_date,
        budget=home.weekly_budget,
        num_items=num_items,
        num_portions_per_recipe=home.num_residents,
        num_pescatarian=0,
        num_vegetarian=0,
        grace_period_weeks=home.num_weeks_recipe_rotation,
        home_id=home.id,
    )


@transaction.atomic
def create_recipe_plan(
    *,
    title: str,
    description: str | None = None,
    from_date: date,
    budget: Decimal,
    num_portions_per_recipe: int,
    num_items: int,
    num_pescatarian: int,
    num_vegetarian: int,
    grace_period_weeks: int | None = None,
    home_id: int | None = None,
) -> None:
    plan_slug = slugify(title)
    recipe_plan = RecipePlan.objects.create(
        title=title,
        description=description,
        slug=plan_slug,
        from_date=from_date,
        home_id=home_id,
    )

    applicable_recipes = find_recipes_applicable_for_plan(
        grace_period_weeks=grace_period_weeks
    )
    plan_distributor = PlanDistributor(
        budget=budget,
        total_num_recipes=num_items,
        num_portions_per_recipe=num_portions_per_recipe,
        num_pescatarian=num_pescatarian,
        num_vegetarian=num_vegetarian,
        applicable_recipes=applicable_recipes,
    )

    recipes_for_plan = plan_distributor.create_plan()

    transaction.on_commit(
        functools.partial(
            _create_recipe_plan_items,
            plan_id=recipe_plan.id,
            recipes=recipes_for_plan,
        )
    )


def _create_recipe_plan_items(
    *, plan_id: int, recipes: list[RecipeDetailRecord]
) -> None:
    plan_items_to_create: list[RecipePlanItem] = []
    ordering = getattr(
        RecipePlanItem.objects.filter(recipe_plan_id=plan_id).last(), "ordering", 1
    )

    for recipe in recipes:
        plan_items_to_create.append(
            RecipePlanItem(
                recipe_plan_id=plan_id,
                recipe_id=recipe.id,
                ordering=ordering,
            )
        )

        ordering += 1

    RecipePlanItem.objects.bulk_create(plan_items_to_create)
