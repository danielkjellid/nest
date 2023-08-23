from .models import RecipeIngredientItemGroup
from .records import (
    RecipeIngredientItemGroupRecord,
)


def get_ingredient_item_groups_for_recipe(
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
    records = [RecipeIngredientItemGroupRecord.from_group(group) for group in groups]

    return records
