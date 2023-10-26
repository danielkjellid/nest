from typing import Iterable

from django.db.models import Q, QuerySet

from nest.core.exceptions import ApplicationError
from nest.core.types import FetchedResult
from nest.ingredients.records import IngredientRecord
from nest.units.records import UnitRecord

from .enums import RecipeDifficulty, RecipeStatus
from .models import Recipe, RecipeIngredientItem, RecipeIngredientItemGroup, RecipeStep
from .records import (
    RecipeDetailRecord,
    RecipeDurationRecord,
    RecipeIngredientItemGroupRecord,
    RecipeIngredientItemRecord,
    RecipeRecord,
    RecipeStepRecord,
)


def _get_ingredient_items(expression: Q) -> QuerySet[RecipeIngredientItem]:
    """
    Get ingredient items with all necessary prefetches to fill out a
    RecipeIngredientItemRecord.
    """
    ingredient_items = (
        RecipeIngredientItem.objects.filter(expression)
        .select_related("ingredient_group", "step")
        .prefetch_related(
            "portion_quantity_unit",
            "ingredient",
            "ingredient__product",
            "ingredient__product__unit",
        )
    )

    return ingredient_items


def get_ingredient_items_for_groups(
    *, group_ids: Iterable[int]
) -> FetchedResult[list[RecipeIngredientItemRecord]]:
    """
    Get a list of RecipeIngredientItemRecord that based on related ingredient group.
    """
    records: FetchedResult[list[RecipeIngredientItemRecord]] = {}

    for item_group_id in group_ids:
        records[item_group_id] = []

    ingredient_items = _get_ingredient_items(Q(ingredient_group_id__in=group_ids))

    for item in ingredient_items:
        records[item.ingredient_group_id].append(
            RecipeIngredientItemRecord(
                id=item.id,
                group_title=item.ingredient_group.title,
                ingredient=IngredientRecord.from_db_model(item.ingredient),
                additional_info=item.additional_info,
                portion_quantity=item.portion_quantity,
                portion_quantity_unit=UnitRecord.from_unit(item.portion_quantity_unit),
                portion_quantity_display="{:f}".format(
                    item.portion_quantity.normalize()
                ),
            )
        )

    return records


def get_ingredient_items_for_steps(
    *, step_ids: Iterable[int]
) -> FetchedResult[list[RecipeIngredientItemRecord]]:
    """
    Get a list of RecipeIngredientItemRecord that based on related steps.
    """
    records: FetchedResult[list[RecipeIngredientItemRecord]] = {}

    for step_id in step_ids:
        records[step_id] = []

    ingredient_items = _get_ingredient_items(Q(step_id__in=step_ids))

    for item in ingredient_items:
        item_step_id = getattr(item, "step_id", None)

        if item_step_id is None:
            continue

        records[item_step_id].append(
            RecipeIngredientItemRecord(
                id=item.id,
                group_title=item.ingredient_group.title,
                ingredient=IngredientRecord.from_db_model(item.ingredient),
                additional_info=item.additional_info,
                portion_quantity=item.portion_quantity,
                portion_quantity_unit=UnitRecord.from_unit(item.portion_quantity_unit),
                portion_quantity_display="{:f}".format(
                    item.portion_quantity.normalize()
                ),
            )
        )

    return records


def get_ingredient_item_groups_for_recipes(
    *,
    recipe_ids: Iterable[int],
) -> FetchedResult[list[RecipeIngredientItemGroupRecord]]:
    """
    Get a list of ingredient item group for a list of recipes. Returns a dict where the
    recipe id is key and a list of RecipeIngredientItemGroupRecord is value.
    """
    records: FetchedResult[list[RecipeIngredientItemGroupRecord]] = {}

    # Prefill all recipes passed in so that we always return a result for them.
    for recipe_id in recipe_ids:
        records[recipe_id] = []

    item_groups = RecipeIngredientItemGroup.objects.filter(
        recipe_id__in=recipe_ids
    ).order_by("ordering")

    item_group_ids = item_groups.values_list("id", flat=True)
    ingredient_items = get_ingredient_items_for_groups(group_ids=item_group_ids)

    for item_group in item_groups:
        records[item_group.recipe_id].append(
            RecipeIngredientItemGroupRecord(
                id=item_group.id,
                title=item_group.title,
                ordering=item_group.ordering,
                ingredient_items=ingredient_items[item_group.id],
            )
        )

    return records


def get_ingredient_item_groups_for_recipe(
    *, recipe_id: int
) -> list[RecipeIngredientItemGroupRecord]:
    """
    Get ingredient item groups for a single recipe.
    """
    ingredient_group = get_ingredient_item_groups_for_recipes(recipe_ids=[recipe_id])

    return ingredient_group[recipe_id]


def get_steps_for_recipes(
    *, recipe_ids: Iterable[int]
) -> FetchedResult[list[RecipeStepRecord]]:
    """
    Get a list of steps for a list of recipes. Returns a dict where the
    recipe id is key and a list of RecipeStepRecord is value.
    """
    records: FetchedResult[list[RecipeStepRecord]] = {}

    for recipe_id in recipe_ids:
        records[recipe_id] = []

    steps = RecipeStep.objects.filter(recipe_id__in=recipe_ids).order_by("number")
    step_ids = steps.values_list("id", flat=True)
    ingredient_items = get_ingredient_items_for_steps(step_ids=step_ids)

    for step in steps:
        records[step.recipe_id].append(
            RecipeStepRecord(
                id=step.id,
                number=step.number,
                duration=step.duration,
                instruction=step.instruction,
                step_type=step.get_step_type(),
                step_type_display=step.get_step_type_display(),
                ingredient_items=ingredient_items[step.id],
            )
        )

    return records


def get_steps_for_recipe(*, recipe_id: int) -> list[RecipeStepRecord]:
    """
    Get steps for a single recipe.
    """
    steps = get_steps_for_recipes(recipe_ids=[recipe_id])

    return steps[recipe_id]


def get_recipe(*, pk: int) -> RecipeDetailRecord:
    """
    Get a recipe instance.
    """
    recipe = Recipe.objects.filter(id=pk).annotate_duration().first()

    if not recipe:
        raise ApplicationError(message="Recipe does not exist.")

    steps = get_steps_for_recipe(recipe_id=pk)
    ingredient_groups = get_ingredient_item_groups_for_recipe(recipe_id=pk)

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


def get_recipes() -> list[RecipeRecord]:
    """
    Get a list off all recipes.
    """
    recipes = Recipe.objects.all().order_by("-created_at")
    records = [RecipeRecord.from_recipe(recipe) for recipe in recipes]

    return records
