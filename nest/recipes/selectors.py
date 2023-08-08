from .records import RecipeIngredientRecord
from .models import RecipeIngredient


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
