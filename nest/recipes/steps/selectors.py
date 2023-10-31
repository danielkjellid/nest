from typing import Iterable

from nest.core.types import FetchedResult

from ..ingredients.selectors import get_recipe_ingredient_items_for_steps
from .models import RecipeStep
from .records import RecipeStepRecord


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
    ingredient_items = get_recipe_ingredient_items_for_steps(
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
