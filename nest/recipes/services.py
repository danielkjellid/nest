from .models import (
    Recipe,
    RecipeIngredientItem,
    RecipeIngredientItemGroup,
    RecipeStep,
)
from nest.audit_logs.services import log_create_or_updated
from django.http import HttpRequest
from django.utils.text import slugify
from .enums import RecipeDifficulty, RecipeStatus
from django.db import transaction
from decimal import Decimal
from .types import RecipeIngredientItemGroupDict, RecipeStepDict
from nest.core.exceptions import ApplicationError
from datetime import timedelta
from .enums import RecipeStepType
from .records import RecipeRecord


def create_recipe(
    *,
    title: str,
    search_keywords: str,
    status: RecipeStatus | str,
    difficulty: RecipeDifficulty | str,
    default_num_portions: int | str = 4,
    external_id: str | None = None,
    external_url: str | None = None,
    is_partial_recipe: bool = False,
    is_vegetarian: bool = False,
    is_pescatarian: bool = False,
    request: HttpRequest | None = None,
) -> RecipeRecord:
    """
    Create a single recipe instance.
    """
    slug = slugify(value=title)

    if isinstance(status, str):
        status = RecipeStatus(int(status))

    if isinstance(difficulty, str):
        difficulty = RecipeDifficulty(int(difficulty))

    recipe = Recipe(
        title=title,
        slug=slug,
        search_keywords=search_keywords,
        default_num_portions=default_num_portions,
        status=status,
        difficulty=difficulty,
        external_id=external_id,
        external_url=external_url,
        is_partial_recipe=is_partial_recipe,
        is_vegetarian=is_vegetarian,
        is_pescatarian=is_pescatarian,
    )
    recipe.full_clean()
    recipe.save()

    log_create_or_updated(old=None, new=recipe, request_or_user=request)
    return RecipeRecord.from_recipe(recipe)


def create_ingredient_item_groups(
    *, recipe_id: int | str, ingredient_group_items: list[RecipeIngredientItemGroupDict]
) -> None:
    """
    Create ingredient item groups and related ingredient items and associate them with a
    recipe.
    """

    # Sanity check that we only are dealing with unique ordering properties.
    ordering = [group["ordering"] for group in ingredient_group_items]
    if not len(set(ordering)) == len(ordering):
        raise ApplicationError(
            message="Ordering for ingredient group items has to be unique"
        )

    # Sanity check that we are only dealing with unique instructions.
    titles = [group["title"] for group in ingredient_group_items]
    if not len(set(titles)) == len(titles):
        raise ApplicationError(
            message="Titles for ingredient group items has to be unique"
        )

    # Create a list of which ingredient_group_items to bulk create.
    recipe_ingredient_groups_to_create = [
        RecipeIngredientItemGroup(
            recipe_id=recipe_id,
            title=item_group["title"],
            ordering=item_group["ordering"],
        )
        for item_group in ingredient_group_items
    ]

    # Do all transactions atomically so that we can take advantage of the on_commit
    # callback.
    with transaction.atomic():
        # Create ingredient_item_groups.
        created_ingredient_item_groups = RecipeIngredientItemGroup.objects.bulk_create(
            recipe_ingredient_groups_to_create
        )

        try:
            ingredient_items_to_create = [
                RecipeIngredientItem(
                    # Try to find associated group though generator, as created_
                    # ingredient_item_groups should return a list of created objects.
                    ingredient_group_id=next(
                        group.id
                        for group in created_ingredient_item_groups
                        if group.title == item_group["title"]
                        and group.ordering == item_group["ordering"]
                    ),
                    ingredient_id=ingredient_item["ingredient_id"],
                    additional_info=(
                        ingredient_item["additional_info"]
                        if ingredient_item["additional_info"]
                        else None
                    ),
                    portion_quantity=Decimal(ingredient_item["portion_quantity"]),
                    portion_quantity_unit_id=int(
                        ingredient_item["portion_quantity_unit_id"]
                    ),
                )
                for item_group in ingredient_group_items
                for ingredient_item in item_group["ingredients"]
            ]
        except StopIteration as exc:
            raise ApplicationError(
                message="Could not find group to connect to ingredient item."
            ) from exc

        def create_ingredient_items() -> None:
            RecipeIngredientItem.objects.bulk_create(ingredient_items_to_create)

        # Once groups has been created, use callback to create associated
        # ingredient_items.
        transaction.on_commit(create_ingredient_items)


def create_recipe_steps(*, recipe_id: int | str, steps: list[RecipeStepDict]) -> None:
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
            step_type=RecipeStepType(int(step["step_type"])),
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
