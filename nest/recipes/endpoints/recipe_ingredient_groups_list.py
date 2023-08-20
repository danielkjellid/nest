from django.http import HttpRequest
from ninja import Schema

from nest.api.responses import APIResponse
from ..selectors import get_ingredient_item_groups_for_recipe

from .router import router


class RecipeIngredientProductListOut(Schema):
    full_name: str
    thumbnail_url: str | None


# TODO: Naming!
class RecipeIngredientListOut(Schema):
    id: int
    title: str
    product: RecipeIngredientProductListOut


class RecipeIngredientItemPortionUnitListOut(Schema):
    abbreviation: str


class RecipeIngredientItemListOut(Schema):
    id: int
    ingredient: RecipeIngredientListOut
    portion_quantity_unit: RecipeIngredientItemPortionUnitListOut


class RecipeIngredientItemGroupListOut(Schema):
    id: int
    title: str
    ingredient_items: list[RecipeIngredientItemListOut]


@router.get(
    "{recipe_id}/ingredient-groups/",
    response=APIResponse[list[RecipeIngredientItemGroupListOut]],
)
def recipe_ingredient_groups_list_api(request: HttpRequest, recipe_id: int):
    """
    Get a list of all RecipeIngredientItemGroups for a recipe.
    """

    groups = get_ingredient_item_groups_for_recipe(recipe_id=recipe_id)
    data = [RecipeIngredientItemGroupListOut(**group.dict()) for group in groups]

    return APIResponse(status="success", data=data)
