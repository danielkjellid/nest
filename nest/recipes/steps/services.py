from nest.core.exceptions import ApplicationError
from .models import RecipeStep
from datetime import timedelta
from .enums import RecipeStepType
from ..ingredients.models import RecipeIngredientItem
from typing import Any


def create_recipe_steps(*, recipe_id: int | str, steps: list[dict[str, Any]]) -> None:
    """
    Create steps related to a single recipe instance.
    """

    # Get all step numbers from payload to run som sanity checks.
    step_numbers = sorted([step["number"] for step in steps])

    # Sanity check that there is a "step 1" in the payload.
    if not step_numbers[0] == 1:
        raise ApplicationError(
            message="Steps payload has to include step with number 1"
        )

    # Sanity check that step numbers are in sequence.
    if not set(step_numbers) == set(range(min(step_numbers), max(step_numbers) + 1)):
        raise ApplicationError(message="Step numbers has to be in sequence.")

    # Sanity check that all instruction fields have content.
    if any(not step["instruction"] for step in steps):
        raise ApplicationError(message="All steps has to have instructions defined.")

    ingredient_items_to_update = []
    ingredient_item_ids = [
        int(item_id) for step in steps for item_id in step["ingredient_items"]
    ]
    ingredient_items = list(
        RecipeIngredientItem.objects.filter(
            ingredient_group__recipe_id=recipe_id, id__in=ingredient_item_ids
        )
    )

    recipe_steps_to_create = [
        RecipeStep(
            recipe_id=recipe_id,
            number=step["number"],
            duration=timedelta(minutes=step["duration"]),
            instruction=step["instruction"],
            step_type=RecipeStepType(step["step_type"]),
        )
        for step in steps
    ]
    created_recipe_steps = RecipeStep.objects.bulk_create(recipe_steps_to_create)

    for step in steps:
        # Find related step that has been created to get appropriate id to attach to
        # the ingredient item.
        created_step = next(
            (
                created_step
                for created_step in created_recipe_steps
                if step["number"] == created_step.number
                and step["instruction"] == created_step.instruction
            ),
            None,
        )

        if not created_step:
            continue

        items = [
            item
            for item in ingredient_items
            if item.id
            in [int(step_item_id) for step_item_id in step["ingredient_items"]]
        ]

        for item in items:
            if item.step_id is not None:
                continue

            item.step_id = created_step.id
            ingredient_items_to_update.append(item)

    # Update ingredient items with new step_ids in bulk.
    RecipeIngredientItem.objects.bulk_update(ingredient_items_to_update, ["step"])
