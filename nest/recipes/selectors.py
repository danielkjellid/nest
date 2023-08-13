from .records import RecipeIngredientRecord, RecipeIngredientItemGroupRecord
from .models import RecipeIngredient, RecipeIngredientItem, RecipeIngredientItemGroup


def get_ingredients() -> list[RecipeIngredientRecord]:
    """
    Get a list of all ingredients in the application.
    """
    ingredients = RecipeIngredient.objects.all().select_related("product")
    records = [
        RecipeIngredientRecord.from_ingredient(ingredient=ingredient)
        for ingredient in ingredients
    ]

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
            "ingredient_items",
            "ingredient_items__portion_quantity_unit",
            "ingredient_items__ingredient",
            "ingredient_items__ingredient__product",
            "ingredient_items__ingredient__product__unit",
        )
        .order_by("ordering")
    )
    records = [RecipeIngredientItemGroupRecord.from_group(group) for group in groups]

    return records
