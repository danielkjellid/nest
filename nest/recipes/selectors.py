from .records import (
    RecipeIngredientRecord,
    RecipeIngredientItemGroupRecord,
)
from .models import RecipeIngredient, Recipe, RecipeIngredientItemGroup


def get_ingredients() -> list[RecipeIngredientRecord]:
    """
    Get a list of all ingredients in the application.
    """
    ingredients = RecipeIngredient.objects.all().select_related("product__unit")
    # records = [
    #     RecipeIngredientRecord.from_ingredient(ingredient=ingredient)
    #     for ingredient in ingredients
    # ]
    records = []

    return records


def get_ingredient_group_items_for_recipe(
    *, recipe_id: str | int
) -> list[RecipeIngredientItemGroupRecord]:
    """
    Get a list of all RecipeIngredientItemGroups connected to a specific recipe.
    """
    groups = (
        RecipeIngredientItemGroup.objects.filter(recipe_id=recipe_id)
        .prefetch_related(
            "ingredient_items__portion_quantity_unit",
            "ingredient_items__ingredient__product__unit",
        )
        .order_by("ordering")
    )
    # records = [RecipeIngredientItemGroupRecord.from_group(group) for group in groups]
    records = []

    return records


def get_recipes() -> list[int]:
    recipes = Recipe.objects.all().prefetch_related(
        "steps__ingredient_items__portion_quantity_unit",
        "steps__ingredient_items__ingredient__product__unit",
        "ingredient_groups__ingredient_items__portion_quantity_unit",
        "ingredient_groups__ingredient_items__ingredient__product__unit",
    )
    # records = [RecipeDetailRecord.from_recipe(recipe=recipe) for recipe in recipes]
    records = []

    return records
