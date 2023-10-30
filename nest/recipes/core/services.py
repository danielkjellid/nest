from django.http import HttpRequest
from django.utils.text import slugify

from nest.audit_logs.services import log_create_or_updated

from .enums import RecipeDifficulty, RecipeStatus
from .models import Recipe
from .records import RecipeRecord


def create_recipe(
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
