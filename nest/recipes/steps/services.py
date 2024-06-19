from __future__ import annotations

import functools
from datetime import timedelta
from decimal import Decimal

import structlog
from django.db import models, transaction
from pydantic import BaseModel

from nest.core.exceptions import ApplicationError

from ..ingredients.models import RecipeIngredientItem
from ..ingredients.services import IngredientItem
from .enums import RecipeStepType
from .models import RecipeStep, RecipeStepIngredientItem

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


@transaction.atomic
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

    transaction.on_commit(
        functools.partial(
            create_or_update_recipe_step_ingredient_items,
            recipe_id=recipe_id,
            steps=steps,
        )
    )


def _find_ingredient_item_id_for_step_item(
    item: IngredientItem,
    recipe_ingredient_items: models.QuerySet[RecipeIngredientItem],
) -> int:
    if item.id is not None:
        return item.id

    item_id = next(
        i.id
        for i in recipe_ingredient_items
        if i.ingredient_id == int(item.ingredient_id)
        and i.portion_quantity == Decimal(item.portion_quantity)
        and i.portion_quantity_unit_id == int(item.portion_quantity_unit_id)
        and i.additional_info == item.additional_info
    )

    return item_id


def _find_step_id_for_step_item(
    step: Step, recipe_steps: models.QuerySet[RecipeStep]
) -> int:
    if step.id is not None:
        return step.id

    step_id = next(
        s.id
        for s in recipe_steps
        if s.number == step.number
        and s.duration == timedelta(minutes=step.duration)
        and s.step_type == step.step_type
    )

    return step_id


def create_or_update_recipe_step_ingredient_items(
    recipe_id: int, steps: list[Step]
) -> None:
    recipe_steps = RecipeStep.objects.filter(recipe_id=recipe_id)
    recipe_ingredient_items = RecipeIngredientItem.objects.filter(
        ingredient_group__recipe_id=recipe_id
    )
    existing_relations = list(
        RecipeStepIngredientItem.objects.filter(step__recipe_id=recipe_id)
    )

    steps_to_ignore: list[int] = []
    relations_to_create: list[RecipeStepIngredientItem] = []

    try:
        for step in steps:
            step_id = _find_step_id_for_step_item(step=step, recipe_steps=recipe_steps)
            for ingredient_item in step.ingredient_items:
                ingredient_item_id = _find_ingredient_item_id_for_step_item(
                    item=ingredient_item,
                    recipe_ingredient_items=recipe_ingredient_items,
                )

                existing_relation = next(
                    (
                        step_ingredient_item
                        for step_ingredient_item in existing_relations
                        if step_ingredient_item.step_id == step_id
                        and step_ingredient_item.ingredient_item_id
                        == ingredient_item_id
                    ),
                    None,
                )

                # Relation already exist, not point in adding it again.
                if existing_relation is not None:
                    steps_to_ignore.append(step_id)
                    continue

                relations_to_create.append(
                    RecipeStepIngredientItem(
                        step_id=step_id,
                        ingredient_item_id=ingredient_item_id,
                    )
                )

    except StopIteration as exc:
        raise ApplicationError(
            message="Could not find step or ingredient item to create relation."
        ) from exc

    relation_ids_to_delete = [
        step_item.id
        for step_item in existing_relations
        if step_item.step_id not in steps_to_ignore
    ]

    if len(relation_ids_to_delete):
        RecipeStepIngredientItem.objects.filter(id__in=relation_ids_to_delete).delete()

    if len(relations_to_create):
        RecipeStepIngredientItem.objects.bulk_create(relations_to_create)
