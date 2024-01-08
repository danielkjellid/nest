import functools
from typing import Any

from django.db import transaction
from django.http import HttpRequest
from django.utils.text import slugify

from nest.audit_logs.services import log_create_or_updated

from ..ingredients.services import create_recipe_ingredient_item_groups
from ..steps.services import create_recipe_steps
from .enums import RecipeDifficulty, RecipeStatus
from .models import Recipe
from .records import RecipeRecord
from nest.core.exceptions import ApplicationError
from nest.core.services import model_update


def create_base_recipe(
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


def edit_base_recipe(
    *, recipe_id: int, request: HttpRequest, **edits: dict[str, Any]
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
    ingredient_group_items: list[dict[str, Any]],
    steps: list[dict[str, Any]],
    request: HttpRequest | None = None,
) -> None:
    """
    Create a full recipe instance with ingredient items and steps.
    """
    with transaction.atomic():
        recipe = create_base_recipe(
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

        with transaction.atomic():
            # Run ingredient item groups on recipe commit.
            transaction.on_commit(
                functools.partial(
                    create_recipe_ingredient_item_groups,
                    recipe_id=recipe.id,
                    ingredient_group_items=ingredient_group_items,
                )
            )

        # Run step creation on ingredient item groups commit.
        transaction.on_commit(
            functools.partial(create_recipe_steps, recipe_id=recipe.id, steps=steps)
        )
