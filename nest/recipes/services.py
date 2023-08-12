from .records import RecipeIngredientRecord
from .models import RecipeIngredient, Recipe
from nest.audit_logs.services import log_create_or_updated
from django.http import HttpRequest
from django.utils.text import slugify
from .enums import RecipeDifficulty, RecipeStatus


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


def link_ingredients_to_recipe():
    ...
