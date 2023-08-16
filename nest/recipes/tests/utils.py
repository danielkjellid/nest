from ..enums import RecipeDifficulty, RecipeStatus, RecipeStepType
from ..models import (
    Recipe,
    RecipeIngredientItem,
    RecipeIngredientItemGroup,
    RecipeIngredient,
    RecipeStep,
)
from datetime import timedelta
from nest.products.models import Product
from nest.products.tests.utils import create_product
from nest.units.tests.utils import get_unit
from decimal import Decimal
from django.utils.text import slugify


def create_recipe(
    *,
    title: str = "Test recipe",
    default_num_portions: int = 4,
    search_keywords: str | None = None,
    external_id: int | None = None,
    external_url: str | None = None,
    status: RecipeStatus = RecipeStatus.PUBLISHED,
    difficulty: RecipeDifficulty = RecipeDifficulty.MEDIUM,
    is_partial_recipe: bool = False,
    is_vegetarian: bool = False,
    is_pescatarian: bool = False,
) -> Recipe:
    """
    Create a recipe to use in tests.
    """
    recipe, _created = Recipe.objects.get_or_create(
        title=title,
        slug=slugify(title),
        default_num_portions=default_num_portions,
        search_keywords=search_keywords,
        external_id=external_id,
        external_url=external_url,
        status=status,
        difficulty=difficulty,
        is_partial_recipe=is_partial_recipe,
        is_vegetarian=is_vegetarian,
        is_pescatarian=is_pescatarian,
    )

    return recipe


def create_recipe_ingredient_item_group(
    *, recipe: Recipe | None = None, title: str = "Group 1", ordering: int = 1
) -> RecipeIngredientItemGroup:
    """
    Create a recipe ingredient item group to use in tests.
    """

    if not recipe:
        recipe = create_recipe()

    ingredient_item_group = RecipeIngredientItemGroup.objects.create(
        recipe=recipe, title=title, ordering=ordering
    )

    return ingredient_item_group


def create_recipe_ingredient_item(
    *,
    ingredient_group: RecipeIngredientItemGroup | None = None,
    ingredient: RecipeIngredient | None = None,
    step: RecipeStep | None = None,
    additional_info: str | None = None,
    portion_quantity: str = "100.00",
    portion_quantity_unit: str = "g",
) -> RecipeIngredientItem:
    """
    Create a recipe ingredient item to use in tests.
    """
    if not ingredient_group:
        ingredient_group = create_recipe_ingredient_item_group()

    if not ingredient:
        ingredient = create_recipe_ingredient()

    ingredient_item = RecipeIngredientItem.objects.create(
        ingredient_group=ingredient_group,
        ingredient=ingredient,
        step=step,
        additional_info=additional_info,
        portion_quantity=Decimal(portion_quantity),
        portion_quantity_unit=get_unit(portion_quantity_unit),
    )

    return ingredient_item


def create_recipe_ingredient(
    *, title: str = "Test ingredient", product: Product | None = None
) -> RecipeIngredient:
    """
    Create a recipe ingredient to use in tests.
    """
    if not product:
        product = create_product()

    ingredient, _created = RecipeIngredient.objects.get_or_create(
        title=title, product=product
    )

    return ingredient


def create_recipe_step(
    *,
    recipe: Recipe | None = None,
    number: int = 1,
    duration: int = 5,
    instruction: str = "Instruction for step",
    step_type: RecipeStep = RecipeStepType.COOKING,
) -> RecipeStep:
    """
    Create a recipe step to use in tests.
    """
    if not recipe:
        recipe = create_recipe()

    step = RecipeStep.objects.create(
        recipe=recipe,
        number=number,
        duration=timedelta(minutes=duration),
        instruction=instruction,
        step_type=step_type,
    )

    return step
