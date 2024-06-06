from datetime import timedelta
from decimal import Decimal
from typing import Any

import structlog
from django.db import transaction
from pydantic import BaseModel

from nest.core.exceptions import ApplicationError

from ..ingredients.models import RecipeIngredientItem
from .enums import RecipeStepType
from .models import RecipeStep

logger = structlog.get_logger()


class Step(BaseModel):
    id: int | None = None
    number: int
    duration: timedelta
    instruction: str
    step_type: RecipeStepType
    ingredient_items: list[Any]


def _validate_steps(steps: list[Step]):
    # Get all step numbers from payload to run som sanity checks.
    step_numbers = sorted([step.number for step in steps])

    # Sanity check that there is a "step 1" in the payload.
    if not step_numbers[0] == 1:
        raise ApplicationError(
            message="Steps payload has to include step with number 1"
        )

    # Sanity check that step numbers are in sequence.
    if not set(step_numbers) == set(range(min(step_numbers), max(step_numbers) + 1)):
        raise ApplicationError(message="Step numbers has to be in sequence.")

    # Sanity check that all instruction fields have content.
    if any(not step.instruction for step in steps):
        raise ApplicationError(message="All steps has to have instructions defined.")


@transaction.atomic
def _create_or_update_recipe_steps_ingredient_items(recipe_id: int, steps: list[Step]):
    recipe_steps = RecipeStep.objects.filter(recipe_id=recipe_id)

    ingredient_item_ids = [item.id for step in steps for item in step.ingredient_items]
    recipe_ingredient_items = RecipeIngredientItem.objects.filter(
        id__in=ingredient_item_ids
    )
    ingredient_items = {item.id: item for item in recipe_ingredient_items}
    ingredient_items_to_update = []

    for step in steps:
        for ingredient_item in step.ingredient_items:
            recipe_ingredient_item = ingredient_items.get(ingredient_item.id, None)
            recipe_step = next(
                (
                    recipe_step.id
                    for recipe_step in recipe_steps
                    if recipe_step.number == step.number
                    and recipe_step.duration == step.duration
                    and recipe_step.step_type == step.step_type
                ),
                None,
            )

            if not recipe_ingredient_item or not recipe_step:
                logger.warn(
                    "Either ingredient item or step is None, failed to make connection",
                    recipe_id=recipe_id,
                    ingredient_item=recipe_ingredient_item,
                    step=recipe_step,
                )
                continue

            ingredient_items_to_update.append(
                RecipeIngredientItem(
                    id=recipe_ingredient_item.id,
                    step_id=next(
                        (
                            recipe_step.id
                            for recipe_step in recipe_steps
                            if recipe_step.number == step.number
                            and recipe_step.duration == step.duration
                            and recipe_step.step_type == step.step_type
                        ),
                        None,
                    ),
                    ingredient_id=recipe_ingredient_item.ingredient_id,
                    additional_info=recipe_ingredient_item.additional_info,
                    portion_quantity=Decimal(recipe_ingredient_item.portion_quantity),
                    portion_quantity_unit_id=recipe_ingredient_item.portion_quantity_unit_id,
                )
            )

    def modify_ingredient_item() -> None:
        if len(ingredient_items_to_update):
            RecipeIngredientItem.objects.bulk_update(
                ingredient_items_to_update,
                fields=["step_id"],
            )

    transaction.on_commit(modify_ingredient_item)


def create_or_update_recipe_steps(recipe_id: int, steps: list[Step]) -> None:
    if not steps:
        return None

    steps_to_create = []
    steps_to_update = []

    for step in steps:
        step_id = getattr(step, "id", None)
        correct_list = steps_to_update if step_id else steps_to_create
        correct_list.append(
            RecipeStep(
                recipe_id=recipe_id,
                id=step_id,
                number=step.number,
                duration=step.duration,
                instruction=step.instruction,
                step_type=step.step_type,
            )
        )

    _validate_steps(steps)

    if len(steps_to_create):
        RecipeStep.objects.bulk_create(steps_to_create)

    if len(steps_to_update):
        RecipeStep.objects.bulk_update(
            steps_to_update, fields=["number", "duration", "instruction", "step_type"]
        )

    # transaction.on_commit(
    #     functools.partial(
    #         _create_or_update_recipe_steps_ingredient_items,
    #         recipe_id=recipe_id,
    #         steps=steps,
    #     )
    # )


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
    ingredient_items = list(
        RecipeIngredientItem.objects.filter(ingredient_group__recipe_id=recipe_id)
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

        for ingredient_item in step["ingredient_items"]:
            ingredient_item_from_db = next(
                (
                    item
                    for item in ingredient_items
                    if item.ingredient_id == int(ingredient_item["ingredient_id"])
                    and Decimal(item.portion_quantity)
                    == Decimal(ingredient_item["portion_quantity"])
                    and item.portion_quantity_unit_id
                    == int(ingredient_item["portion_quantity_unit_id"])
                    and item.step_id is None
                ),
                None,
            )

            if not ingredient_item_from_db:
                continue

            ingredient_item_from_db.step_id = created_step.id
            ingredient_items_to_update.append(ingredient_item_from_db)

    # Update ingredient items with new step_ids in bulk.
    RecipeIngredientItem.objects.bulk_update(ingredient_items_to_update, ["step"])
