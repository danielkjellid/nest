from datetime import timedelta

from django.utils import timezone

from nest.core.types import FetchedResult
from nest.recipes.core.enums import RecipeStatus
from nest.recipes.core.models import Recipe
from nest.recipes.core.records import RecipeDetailRecord
from nest.recipes.core.selectors import get_recipe_data, get_recipes_by_id
from nest.recipes.plans.models import RecipePlan, RecipePlanItem
from nest.recipes.plans.records import RecipePlanItemRecord, RecipePlanRecord

# Have at least two weeks between recipes being used in plans.
RECIPE_GRACE_PERIOD_WEEKS = 2.0


def find_recipes_applicable_for_plan(
    *, grace_period_weeks: float | None = None
) -> list[RecipeDetailRecord]:
    """
    Find applicable recipes for plans. An applicable recipe is a recipe that is not
    used in another plan in the defined grace period and is published.
    """
    grace_period = grace_period_weeks or RECIPE_GRACE_PERIOD_WEEKS
    first_possible_from_date = timezone.now() - timedelta(weeks=float(grace_period))

    recipes = get_recipe_data(
        qs=Recipe.objects.exclude(
            plan_items__recipe_plan__from_date__lt=first_possible_from_date,
        ).filter(
            status=RecipeStatus.PUBLISHED,
        )
    )

    return list(recipes.values())


def get_recipe_plan_items_for_plans(
    *, plan_ids: list[int]
) -> FetchedResult[list[RecipePlanItemRecord]]:
    """
    Get relevant recipe plan items for a recipe plan.
    """
    result: FetchedResult[list[RecipePlanItemRecord]] = {
        plan_id: [] for plan_id in plan_ids
    }

    plan_items = RecipePlanItem.objects.filter(
        recipe_plan_id__in=plan_ids
    ).select_related("recipe_plan")

    recipe_ids = [plan_item.recipe_id for plan_item in plan_items]
    recipes = get_recipes_by_id(recipe_ids=recipe_ids)

    for plan_item in plan_items:
        plan = plan_item.recipe_plan
        recipe = recipes[plan_item.recipe_id]

        if recipe is None:
            continue

        if plan is None:
            continue

        result[plan_item.recipe_plan_id].append(
            RecipePlanItemRecord(
                id=plan_item.id,
                plan_id=plan.id,
                plan_title=plan.title,
                recipe=recipe,
            )
        )

    return result


def get_recipe_plans_for_home(*, home_id: int) -> list[RecipePlanRecord]:
    """
    Get all recipe plans for a specificed home.
    """
    plans = RecipePlan.objects.filter(home_id=home_id).order_by("-created_at")

    plan_ids = [plan.id for plan in plans]
    plan_items = get_recipe_plan_items_for_plans(plan_ids=plan_ids)

    return [
        RecipePlanRecord(
            id=plan.id,
            title=plan.title,
            description=plan.description,
            slug=plan.slug,
            from_date=plan.from_date,
            items=plan_items[plan.id],
        )
        for plan in plans
    ]
