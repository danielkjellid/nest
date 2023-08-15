from .records import RecipeIngredientRecord
from .models import (
    RecipeIngredient,
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


def create_ingredient(
    *, title: str, product_id: int | str, request: HttpRequest | None = None
) -> RecipeIngredientRecord:
    """
    Create a single ingredient instance.
    """

    ingredient = RecipeIngredient(title=title, product_id=product_id)
    ingredient.full_clean()
    ingredient.save()

    log_create_or_updated(old=None, new=ingredient, request_or_user=request)
    return RecipeIngredientRecord.from_ingredient(ingredient=ingredient)


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
) -> int:  # TODO: Change
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
    return recipe.id


# TODO: return linked records?
# TODO: Should log?
# TODO: Should make sure that title and ordering are unique
def link_ingredient_item_groups_to_recipe(
    *, recipe_id: int | str, ingredient_group_items: list[RecipeIngredientItemGroupDict]
) -> None:
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
                    additional_info=ingredient_item["additional_info"],
                    portion_quantity=Decimal(ingredient_item["portion_quantity"]),
                    portion_quantity_unit_id=ingredient_item[
                        "portion_quantity_unit_id"
                    ],
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


def create_recipe_steps(*, recipe_id: int | str, steps: list[RecipeStepDict]):
    ingredient_items_to_update = []
    ingredient_item_ids = [
        item_id for step in steps for item_id in step["ingredient_items"]
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
            type=RecipeStepType(int(step["type"])),
        )
        for step in steps
    ]
    created_recipe_steps = RecipeStep.objects.bulk_create(recipe_steps_to_create)

    for step in steps:
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
            item for item in ingredient_items if item.id in step["ingredient_items"]
        ]

        for item in items:
            item.step = created_step.id
            ingredient_items_to_update.append(item)

    RecipeIngredientItem.objects.bulk_update(ingredient_items_to_update, ["step"])
