from nest.core.exceptions import ApplicationError

from ..ingredients.selectors import get_recipe_ingredient_item_groups_for_recipe
from ..steps.selectors import get_steps_for_recipe
from .enums import RecipeDifficulty, RecipeStatus
from .models import Recipe
from .records import (
    RecipeDetailRecord,
    RecipeDurationRecord,
    RecipeRecord,
)


def get_recipe(*, pk: int) -> RecipeDetailRecord:
    """
    Get a recipe instance.
    """
    recipe = (
        Recipe.objects.filter(id=pk)
        .annotate_duration()
        .annotate_num_plan_usages()
        .first()
    )

    if not recipe:
        raise ApplicationError(message="Recipe does not exist.")

    steps = get_steps_for_recipe(recipe_id=pk)
    ingredient_groups = get_recipe_ingredient_item_groups_for_recipe(recipe_id=pk)

    return RecipeDetailRecord(
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
        ingredient_item_groups=ingredient_groups,
        steps=steps,
        num_plan_usages=getattr(recipe, "num_plan_usages", 0),
    )


def get_recipes() -> list[RecipeRecord]:
    """
    Get a list off all recipes.
    """
    recipes = Recipe.objects.all().order_by("-created_at")
    records = [RecipeRecord.from_recipe(recipe) for recipe in recipes]

    return records
