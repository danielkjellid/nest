from django.db.models import QuerySet

from ...core.exceptions import ApplicationError
from ...core.types import FetchedResult
from ..ingredients.selectors import (
    get_recipe_ingredient_item_groups_for_recipes,
)
from ..steps.selectors import get_steps_for_recipes
from .enums import RecipeDifficulty, RecipeStatus
from .models import Recipe
from .records import (
    RecipeDetailRecord,
    RecipeDurationRecord,
)


def get_recipe(*, pk: int) -> RecipeDetailRecord:
    """
    Get a recipe instance.
    """
    recipe = get_recipes_by_id(recipe_ids=[pk])[pk]

    if not recipe:
        raise ApplicationError("Recipe was not found", status_code=404)

    return recipe


def get_recipe_data(*, qs: QuerySet[Recipe]) -> FetchedResult[RecipeDetailRecord]:
    """
    Core selector for getting recipes. Takes a filtered queryset as parameter and
    does all annotations and ordering based on that.
    """
    result: FetchedResult[RecipeDetailRecord] = {}

    recipes = (
        qs.annotate_duration()  # type: ignore
        .annotate_num_plan_usages()
        .order_by("-created_at")
    )

    recipe_ids = [recipe.id for recipe in recipes]
    steps = get_steps_for_recipes(recipe_ids=recipe_ids)
    ingredient_groups = get_recipe_ingredient_item_groups_for_recipes(
        recipe_ids=recipe_ids
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


def get_recipes_by_id(
    *, recipe_ids: list[int]
) -> FetchedResult[RecipeDetailRecord | None]:
    """
    Get a retrieved recipes based in provided Ids.
    """

    qs = Recipe.objects.filter(id__in=recipe_ids)
    result: FetchedResult[RecipeDetailRecord | None] = {
        recipe_id: None for recipe_id in recipe_ids
    }
    recipes = get_recipe_data(qs=qs)

    for recipe_id, recipe in recipes.items():
        result[recipe_id] = recipe

    return result


def get_recipes() -> list[RecipeDetailRecord]:
    """
    Get a list off all recipes.
    """

    qs = Recipe.objects.all()
    result = get_recipe_data(qs=qs)
    return [value for value in result.values() if value is not None]
