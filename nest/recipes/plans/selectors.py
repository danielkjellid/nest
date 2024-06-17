from datetime import timedelta

from django.utils import timezone

from nest.recipes.core.enums import RecipeStatus
from nest.recipes.core.models import Recipe
from nest.recipes.core.records import RecipeDetailRecord, RecipeDurationRecord
from nest.recipes.ingredients.selectors import (
    get_recipe_ingredient_item_groups_for_recipes,
)
from nest.recipes.steps.selectors import get_steps_for_recipes

# Have at least two weeks between recipes being used in plans.
RECIPE_GRACE_PERIOD_WEEKS = 2.0


def find_recipes_applicable_for_plan(
    *, grace_period_weeks: float | None = None
) -> list[RecipeDetailRecord]:
    grace_period = grace_period_weeks or RECIPE_GRACE_PERIOD_WEEKS
    first_possible_from_date = timezone.now() - timedelta(weeks=float(grace_period))
    print(first_possible_from_date.date())
    recipes = (
        Recipe.objects.exclude(
            plan_items__recipe_plan__from_date__lt=first_possible_from_date,
        )
        .filter(
            status=RecipeStatus.PUBLISHED,
        )
        .annotate_duration()
        .annotate_num_plan_usages()  # type: ignore
    )

    recipe_ids = [recipe.id for recipe in recipes]
    recipe_ingredient_item_groups = get_recipe_ingredient_item_groups_for_recipes(
        recipe_ids=recipe_ids
    )
    recipe_steps = get_steps_for_recipes(recipe_ids=recipe_ids)

    return [
        RecipeDetailRecord(
            id=recipe.id,
            title=recipe.title,
            slug=recipe.slug,
            default_num_portions=recipe.default_num_portions,
            search_keywords=recipe.search_keywords,
            external_id=recipe.external_id,
            external_url=recipe.external_url,
            status=recipe.status,
            status_display=recipe.get_status_display(),
            difficulty=recipe.difficulty,
            difficulty_display=recipe.get_difficulty_display(),
            is_vegetarian=recipe.is_vegetarian,
            is_pescatarian=recipe.is_pescatarian,
            duration=RecipeDurationRecord.from_db_model(recipe),
            glycemic_data=None,
            health_score=None,
            ingredient_item_groups=recipe_ingredient_item_groups[recipe.id],
            steps=recipe_steps[recipe.id],
            num_plan_usages=getattr(recipe, "num_plan_usages", 0),
        )
        for recipe in recipes
    ]
