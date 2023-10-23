from .models import Recipe, RecipeIngredientItemGroup, RecipeStep
from .records import (
    RecipeIngredientItemGroupRecord,
    RecipeRecord,
    RecipeDetailRecord,
    RecipeStepRecord,
    RecipeDurationRecord,
)
from nest.core.exceptions import ApplicationError
from django.db.models import QuerySet
from nest.core.types import FetchedResult
from .enums import RecipeDifficulty, RecipeStatus


def _get_recipe_ingredient_item_groups(
    *, recipe_id
) -> QuerySet[RecipeIngredientItemGroup]:
    groups = (
        RecipeIngredientItemGroup.objects.filter(recipe_id=recipe_id)
        .prefetch_related(
            "ingredient_items",
            "ingredient_items__portion_quantity_unit",
            "ingredient_items__ingredient",
            "ingredient_items__ingredient__product",
            "ingredient_items__ingredient__product__unit",
        )
        .order_by("ordering")
    )

    return groups


def get_ingredient_item_groups_for_recipes(
    recipe_ids: list[int],
) -> FetchedResult[dict[str, list[RecipeIngredientItemGroupRecord]]]:
    records: FetchedResult[dict[str, list[RecipeIngredientItemGroupRecord]]] = {}

    for recipe_id in recipe_ids:
        records[recipe_id] = []

    item_groups = (
        RecipeIngredientItemGroup.objects.filter(recipe_id__in=recipe_ids)
        .prefetch_related(
            "ingredient_items",
            "ingredient_items__portion_quantity_unit",
            "ingredient_items__ingredient",
            "ingredient_items__ingredient__product",
            "ingredient_items__ingredient__product__unit",
        )
        .order_by("ordering")
    )

    for item_group in item_groups:
        records[recipe_id].append(
            RecipeIngredientItemGroupRecord.from_db_model(item_group)
        )

    return records


def get_ingredient_item_groups_for_recipe(
    recipe_id,
) -> dict[str, RecipeIngredientItemGroupRecord]:
    ingredient_group = get_ingredient_item_groups_for_recipes(recipe_ids=[recipe_id])

    return ingredient_group[recipe_id]


def get_steps_for_recipes(
    recipe_ids: list[int],
) -> FetchedResult[dict[str, list[RecipeStepRecord]]]:
    records: FetchedResult[dict[str, list[RecipeStepRecord]]] = {}

    for recipe_id in recipe_ids:
        records[recipe_id] = []

    steps = RecipeStep.objects.filter(recipe_id__in=recipe_ids).prefetch_related(
        "ingredient_items",
        "ingredient_items__ingredient",
        "ingredient_items__ingredient__product",
        "ingredient_items__portion_quantity_unit",
    )

    for step in steps:
        records[recipe_id].append(RecipeStepRecord.from_db_model(step))

    return records


def get_steps_for_recipe(
    recipe_id: int,
) -> FetchedResult[dict[str, list[RecipeStepRecord]]]:
    steps = get_steps_for_recipes(recipe_ids=[recipe_id])

    return steps[recipe_id]


def get_recipes() -> list[RecipeRecord]:
    """
    Get a list off all recipes.
    """
    recipes = Recipe.objects.all().order_by("-created_at")
    records = [RecipeRecord.from_recipe(recipe) for recipe in recipes]

    return records


def get_recipe(*, pk: int) -> RecipeDetailRecord:
    """
    Get a recipe instance.
    """
    recipe = Recipe.objects.filter(id=pk).annotate_duration().first()
    steps = get_steps_for_recipe(recipe_id=pk)
    ingredient_groups = get_ingredient_item_groups_for_recipe(recipe_id=pk)

    if not recipe:
        raise ApplicationError(message="Recipe does not exist.")

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
        ingredient_groups=ingredient_groups,
        steps=steps,
    )
