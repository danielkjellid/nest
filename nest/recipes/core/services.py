import functools
from typing import Any

from django.db import transaction
from django.http import HttpRequest
from django.utils.text import slugify

from nest.audit_logs.services import log_create_or_updated
from nest.core.exceptions import ApplicationError
from nest.core.services import model_update

from ..ingredients.services import (
    IngredientGroupItem,
    create_or_update_recipe_ingredient_item_groups,
    create_or_update_recipe_ingredient_items,
)
from ..steps.services import Step, create_or_update_recipe_steps
from .enums import RecipeDifficulty, RecipeStatus
from .models import Recipe
from .records import RecipeRecord


def _create_base_recipe(
    *,
    title: str,
    search_keywords: str | None = None,
    status: RecipeStatus | str = RecipeStatus.DRAFT,
    difficulty: RecipeDifficulty | str = RecipeDifficulty.MEDIUM,
    default_num_portions: int | str = 4,
    external_id: str | None = None,
    external_url: str | None = None,
    is_vegetarian: bool = False,
    is_pescatarian: bool = False,
    request: HttpRequest | None = None,
) -> RecipeRecord:
    """
    Create a single recipe instance.
    """
    slug = slugify(value=title)

    if isinstance(status, str):
        status = RecipeStatus(status)

    if isinstance(difficulty, str):
        difficulty = RecipeDifficulty(difficulty)

    recipe = Recipe(
        title=title,
        slug=slug,
        search_keywords=search_keywords if search_keywords else None,
        default_num_portions=default_num_portions,
        status=status,
        difficulty=difficulty,
        external_id=external_id,
        external_url=external_url,
        is_vegetarian=is_vegetarian,
        is_pescatarian=is_pescatarian,
    )
    recipe.full_clean()
    recipe.save()

    log_create_or_updated(old=None, new=recipe, request_or_user=request)
    return RecipeRecord.from_recipe(recipe)


def _edit_base_recipe(
    *, recipe_id: int, request: HttpRequest | None, **edits: dict[str, Any]
) -> None:
    """
    Edit an existing base recipe.
    """

    recipe = Recipe.objects.filter(id=recipe_id).first()

    if not recipe:
        raise ApplicationError(message="Recipe does not exist.")

    data = edits.copy()

    _recipe_instance, _has_updated = model_update(
        instance=recipe, data=data, request=request
    )


@transaction.atomic
def create_recipe(  # noqa: PLR0913
    *,
    title: str,
    search_keywords: str | None = None,
    status: RecipeStatus | str = RecipeStatus.DRAFT,
    difficulty: RecipeDifficulty | str = RecipeDifficulty.MEDIUM,
    default_num_portions: int | str = 4,
    external_id: str | None = None,
    external_url: str | None = None,
    is_vegetarian: bool = False,
    is_pescatarian: bool = False,
    ingredient_group_items: list[IngredientGroupItem],
    steps: list[Step],
    request: HttpRequest | None = None,
) -> None:
    """
    Create a full recipe instance with ingredient items and steps.
    """
    recipe = _create_base_recipe(
        title=title,
        search_keywords=search_keywords,
        status=status,
        difficulty=difficulty,
        default_num_portions=default_num_portions,
        external_id=external_id,
        external_url=external_url,
        is_vegetarian=is_vegetarian,
        is_pescatarian=is_pescatarian,
        request=request,
    )

    transaction.on_commit(
        functools.partial(
            create_or_update_recipe_attributes,
            recipe_id=recipe.id,
            ingredient_item_groups=ingredient_group_items,
            steps=steps,
        )
    )


@transaction.atomic
def create_or_update_recipe_attributes(
    *,
    recipe_id: int,
    ingredient_item_groups: list[IngredientGroupItem],
    steps: list[Step],
) -> None:
    create_or_update_recipe_ingredient_item_groups(
        recipe_id=recipe_id, ingredient_item_groups=ingredient_item_groups
    )

    # Once items groups has been created, create steps and step item relations.
    transaction.on_commit(
        functools.partial(
            create_or_update_recipe_steps,
            recipe_id=recipe_id,
            steps=steps,
        )
    )


@transaction.atomic
def edit_recipe(
    *,
    recipe_id: int,
    base_edits: dict[str, Any] | None = None,
    ingredient_group_items: list[IngredientGroupItem] | None = None,
    steps: list[Step] | None = None,
    request: HttpRequest | None = None,
) -> None:
    """
    Edit an existing recipe instance.
    """
    base_edits = base_edits or {}
    ingredient_group_items = ingredient_group_items or []
    steps = steps or []

    _edit_base_recipe(recipe_id=recipe_id, request=request, **base_edits)

    transaction.on_commit(
        functools.partial(
            create_or_update_recipe_attributes,
            recipe_id=recipe_id,
            ingredient_item_groups=ingredient_group_items,
            steps=steps,
        )
    )
