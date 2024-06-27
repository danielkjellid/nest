from nest.core.exceptions import ApplicationError

from ..ingredients.selectors import (
    get_recipe_ingredient_item_groups_for_recipe,
    get_recipe_ingredient_item_groups_for_recipes,
)
from ..steps.selectors import get_steps_for_recipe, get_steps_for_recipes
from .enums import RecipeDifficulty, RecipeStatus
from .models import Recipe
from .records import (
    RecipeDetailRecord,
    RecipeDurationRecord,
    RecipeRecord,
)
from ...core.types import FetchedResult


def get_recipe(*, pk: int) -> RecipeDetailRecord:
    """
    Get a recipe instance.
    """
    recipe = get_recipes(recipe_ids=[pk])[pk]
    return recipe


def get_recipes(
    *, recipe_ids: list[int] | None = None
) -> FetchedResult[RecipeDetailRecord]:
    """
    Get a list off all recipes.
    """

    result = {recipe_id: None for recipe_id in recipe_ids}

    if not recipe_ids:
        recipes = (
            Recipe.objects.all()
            .annotate_duration()
            .annotate_num_plan_usages()
            .order_by("-created_at")
        )
    else:
        recipes = (
            Recipe.objects.filter(id__in=recipe_ids)
            .annotate_duration()
            .annotate_num_plan_usages()
            .order_by("-created_at")
        )

    relevant_recipe_ids = [recipe.id for recipe in recipes]
    steps = get_steps_for_recipes(recipe_ids=relevant_recipe_ids)
    ingredient_groups = get_recipe_ingredient_item_groups_for_recipes(
        recipe_ids=relevant_recipe_ids
    )

    for recipe in recipes:
        result[recipe.id] = RecipeDetailRecord(
            id=recipe.id,
            title=recipe.title,
            slug=recipe.slug,
            default_num_portions=recipe.default_num_portions,
            search_keywords=recipe.search_keywords,
            external_id=recipe.external_id,
            external_url=recipe.external_url,
            status=RecipeStatus(recipe.status),
            status_display=recipe.get_status_display(),
            difficulty=RecipeDifficulty(recipe.difficulty),
            difficulty_display=recipe.get_difficulty_display(),
            is_vegetarian=recipe.is_vegetarian,
            is_pescatarian=recipe.is_pescatarian,
            duration=RecipeDurationRecord.from_db_model(recipe),
            glycemic_data=None,
            health_score=None,
            ingredient_item_groups=ingredient_groups[recipe.id],
            steps=steps[recipe.id],
            num_plan_usages=getattr(recipe, "num_plan_usages", 0),
        )

    return result
