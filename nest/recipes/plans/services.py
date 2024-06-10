import functools
from datetime import date, timedelta
from decimal import Decimal

from django.db import transaction
from django.utils.text import slugify

from nest.recipes.core.records import RecipeRecord
from nest.recipes.plans.models import RecipePlan, RecipePlanItem
from nest.recipes.plans.selectors import find_recipes_applicable_for_plan


def create_weekly_recipe_plan(
    *, from_date: date, num_items: int = 7, auto_generated: bool = False
):
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
        num_items=num_items,
    )


@transaction.atomic
def create_recipe_plan(
    *,
    title: str,
    description: str | None = None,
    from_date: date,
    num_items: int,
    num_pescatarian: int,
    num_vegetarian: int,
    monetary_cap: Decimal,
):
    plan_slug = slugify(title)
    recipe_plan = RecipePlan.objects.create(
        title=title,
        description=description,
        slug=plan_slug,
        from_date=from_date,
    )

    transaction.on_commit(
        functools.partial(
            _create_recipe_plan_items,
            plan_id=recipe_plan.od,
        )
    )


def _create_recipe_plan_items(plan_id: int) -> None:
    plan_items_to_create: list[RecipePlanItem] = []
    ordering = getattr(
        RecipePlanItem.objects.filter(recipe_plan_id=plan_id).last(), "ordering", 1
    )

    recipes = find_recipes_applicable_for_plan(plan_id=plan_id)

    normal_recipes = []
    pescatarian_recipes = []
    vegetarian_recipes = []

    for recipe in recipes:
        if recipe.is_vegetarian:
            vegetarian_recipes.append(recipe)
        elif recipe.is_pescatarian:
            pescatarian_recipes.append(recipe)
        else:
            normal_recipes.append(recipe)

    for recipe in recipes:
        plan_items_to_create.append(
            RecipePlanItem(
                recipe_plan_id=plan_id,
                recipe_id=recipe.id,
                ordering=ordering,
            )
        )

        ordering += 1

    # TODO: assert ordering unique

    RecipePlanItem.objects.bulk_create(plan_items_to_create)