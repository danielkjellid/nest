from datetime import timedelta

from django.utils import timezone

from nest.recipes.core.enums import RecipeStatus
from nest.recipes.core.models import Recipe
from nest.recipes.core.records import RecipeRecord

# Have at least two weeks between recipes being used in plans.
RECIPE_GRACE_PERIOD_WEEKS = 2


def find_recipes_applicable_for_plan(
    plan_id: int, num_recipes: int
) -> list[RecipeRecord]:
    first_possible_from_date = timezone.now() - timedelta(
        weeks=RECIPE_GRACE_PERIOD_WEEKS
    )
    recipes = Recipe.objects.exclude(
        status=RecipeStatus.PUBLISHED,
        plan_items__recipe_plan_id=plan_id,
        plan_items__recipe_plan__from_date__lte=first_possible_from_date,
    )[:num_recipes]

    assert (
        len(recipes) == num_recipes
    ), "Could not find enough recipes applicable to weekly plan."

    return [
        RecipeRecord(
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
        )
        for recipe in recipes
    ]
