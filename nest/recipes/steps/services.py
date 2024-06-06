from __future__ import annotations

from datetime import timedelta

import structlog
from pydantic import BaseModel

from nest.core.exceptions import ApplicationError

from ..ingredients.services import IngredientItem
from .enums import RecipeStepType
from .models import RecipeStep

logger = structlog.get_logger()


class Step(BaseModel):
    id: int | None = None
    number: int
    duration: int
    instruction: str
    step_type: RecipeStepType
    ingredient_items: list[IngredientItem]


def _validate_steps(steps: list[Step]) -> None:
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


def create_or_update_recipe_steps(recipe_id: int, steps: list[Step]) -> None:
    if not steps:
        return None

    steps_to_create: list[RecipeStep] = []
    steps_to_update: list[RecipeStep] = []

    for step in steps:
        step_id = getattr(step, "id", None)
        correct_list = steps_to_update if step_id is not None else steps_to_create
        correct_list.append(
            RecipeStep(
                recipe_id=recipe_id,
                id=step_id,
                number=step.number,
                duration=timedelta(minutes=step.duration),
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
