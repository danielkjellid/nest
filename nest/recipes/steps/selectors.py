from typing import Iterable

from nest.core.types import FetchedResult
from ..ingredients.records import RecipeIngredientItemRecord, RecipeIngredientRecord

from .models import RecipeStep, RecipeStepIngredientItem
from .records import RecipeStepRecord
from ...units.records import UnitRecord


def get_step_ingredient_items_for_steps(
    *, step_ids: list[int]
) -> FetchedResult[list[RecipeIngredientItemRecord]]:
    """
    Get a list of RecipeIngredientItemRecord that based on related steps.
    """
    records: FetchedResult[list[RecipeIngredientItemRecord]] = {}

    for step_id in step_ids:
        records[step_id] = []

    step_ingredient_items = RecipeStepIngredientItem.objects.filter(
        step_id__in=step_ids
    ).select_related("ingredient_item__ingredient__product__unit")

    for step_ingredient_item in step_ingredient_items:
        if step_ingredient_item.ingredient_item is None:
            continue

        item = step_ingredient_item.ingredient_item
        records[step_ingredient_item.step_id].append(
            RecipeIngredientItemRecord(
                id=item.id,
                group_title=item.ingredient_group.title,
                ingredient=RecipeIngredientRecord.from_db_model(item.ingredient),
                additional_info=item.additional_info,
                portion_quantity=item.portion_quantity,
                portion_quantity_unit=UnitRecord.from_unit(item.portion_quantity_unit),
                portion_quantity_display="{:f}".format(
                    item.portion_quantity.normalize()
                ),
            )
        )

    return records


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
    ingredient_items = get_step_ingredient_items_for_steps(
        step_ids=[step.id for step in steps]
    )

    for step in steps:
        records[step.recipe_id].append(
            RecipeStepRecord(
                id=step.id,
                number=step.number,
                duration=step.duration,
                instruction=step.instruction,
                step_type=step.get_step_type,
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
