from django.utils.text import slugify

from ..enums import RecipeDifficulty, RecipeStatus
from ..models import Recipe


def create_recipe(
    *,
    title: str = "Test recipe",
    default_num_portions: int = 4,
    search_keywords: str | None = None,
    external_id: int | None = None,
    external_url: str | None = None,
    status: RecipeStatus = RecipeStatus.PUBLISHED,
    difficulty: RecipeDifficulty = RecipeDifficulty.MEDIUM,
    is_vegetarian: bool = False,
    is_pescatarian: bool = False,
) -> Recipe:
    """
    Create a recipe to use in tests.
    """
    recipe = Recipe.objects.create(
        title=title,
        slug=slugify(title),
        default_num_portions=default_num_portions,
        search_keywords=search_keywords,
        external_id=external_id,
        external_url=external_url,
        status=status,
        difficulty=difficulty,
        is_vegetarian=is_vegetarian,
        is_pescatarian=is_pescatarian,
    )

    return recipe
