from .models import Ingredient
from .records import IngredientRecord


def get_ingredients() -> list[IngredientRecord]:
    """
    Get a list of all ingredients in the application.
    """
    ingredients = Ingredient.objects.all().select_related("product__unit")
    records = [
        IngredientRecord.from_ingredient(ingredient=ingredient)
        for ingredient in ingredients
    ]

    return records
