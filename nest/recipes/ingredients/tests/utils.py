from decimal import Decimal

from nest.products.core.models import Product
from nest.products.core.tests.utils import create_product
from nest.recipes.core.models import Recipe
from nest.recipes.core.tests.utils import create_recipe
from nest.recipes.steps.models import RecipeStep
from nest.units.tests.utils import get_unit

from ..models import RecipeIngredient, RecipeIngredientItem, RecipeIngredientItemGroup


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
