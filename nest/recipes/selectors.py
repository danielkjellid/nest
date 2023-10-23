from .models import Recipe, RecipeIngredientItemGroup, RecipeStep
from .records import (
    RecipeIngredientItemGroupRecord,
    RecipeRecord,
    RecipeDetailRecord,
    RecipeStepRecord,
    RecipeStepDisplayRecord,
    RecipeIngredientItemGroupDisplayRecord,
    RecipeIngredientItemRecord,
)
from nest.ingredients.records import IngredientRecord
from .enums import RecipeStatus, RecipeDifficulty
from nest.core.exceptions import ApplicationError
from nest.units.records import UnitRecord
from django.db.models import QuerySet
from nest.core.decorators import ensure_prefetched_relations2
from nest.core.types import FetchedResult


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


AnyIngredientGroup = (
    RecipeIngredientItemGroupRecord | RecipeIngredientItemGroupDisplayRecord
)


def get_ingredient_item_groups_for_recipes(
    recipe_ids: list[int],
) -> FetchedResult[dict[str, list[AnyIngredientGroup]]]:
    records: FetchedResult[dict[str, list[AnyIngredientGroup]]] = {}

    for recipe_id in recipe_ids:
        records[recipe_id] = {"normal": [], "display": []}

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
        records[recipe_id]["normal"].append(
            RecipeIngredientItemGroupRecord.from_db_model(item_group)
        )
        records[recipe_id]["display"].append(
            RecipeIngredientItemGroupDisplayRecord.from_db_model(item_group)
        )

    return records


def get_ingredient_item_groups_for_recipe(recipe_id) -> dict[str, AnyIngredientGroup]:
    ingredient_group = get_ingredient_item_groups_for_recipes(recipe_ids=[recipe_id])

    return ingredient_group[recipe_id]


AnyStep = RecipeStepRecord | RecipeStepDisplayRecord


def get_steps_for_recipes(
    recipe_ids: list[int],
) -> FetchedResult[dict[str, list[AnyStep]]]:
    records: FetchedResult[dict[str, list[AnyStep]]] = {}

    for recipe_id in recipe_ids:
        records[recipe_id] = {"normal": [], "display": []}

    steps = RecipeStep.objects.filter(recipe_id__in=recipe_ids).prefetch_related(
        "ingredient_items"
    )

    for step in steps:
        records[recipe_id]["normal"].append(RecipeStepRecord.from_db_model(step))
        records[recipe_id]["display"].append(
            RecipeStepDisplayRecord.from_db_model(step)
        )

    return records


def get_steps_for_recipe(recipe_id: int) -> FetchedResult[dict[str, list[AnyStep]]]:
    steps = get_steps_for_recipes(recipe_ids=[recipe_id])

    return steps[recipe_id]


def _get_recipe_steps(*, recipe_id: int) -> QuerySet[RecipeStep]:
    steps = RecipeStep.objects.filter(recipe_id=recipe_id).prefetch_related(
        "ingredient_items"
    )

    return steps


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

    return RecipeDetailRecord.from_db_model(
        model=recipe,
        ingredient_groups=ingredient_groups["normal"],
        ingredient_groups_display=ingredient_groups["display"],
        steps=steps["normal"],
        steps_display=steps["display"],
    )
