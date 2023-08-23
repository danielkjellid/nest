from django.http import HttpRequest
from ninja import Schema
from pydantic import parse_obj_as

from nest.api.responses import APIResponse

from ..selectors import get_ingredient_item_groups_for_recipe
from .router import router


class RecipeIngredientGroupsListIngredientProductOut(Schema):
    full_name: str
    thumbnail_url: str | None


class RecipeIngredientGroupsListIngredientOut(Schema):
    id: int
    title: str
    product: RecipeIngredientGroupsListIngredientProductOut


class RecipeIngredientGroupsListItemPortionQuantityUnitOut(Schema):
    abbreviation: str


class RecipeIngredientGroupsListItemOut(Schema):
    id: int
    ingredient: RecipeIngredientGroupsListIngredientOut
    portion_quantity_unit: RecipeIngredientGroupsListItemPortionQuantityUnitOut


class RecipeIngredientGroupsListOut(Schema):
    id: int
    title: str
    ingredient_items: list[RecipeIngredientGroupsListItemOut]


@router.get(
    "{recipe_id}/ingredient-groups/",
    response=APIResponse[list[RecipeIngredientGroupsListOut]],
)
def recipe_ingredient_groups_list_api(
    request: HttpRequest, recipe_id: int
) -> APIResponse[list[RecipeIngredientGroupsListOut]]:
    """
    Get a list of all RecipeIngredientItemGroups for a recipe.
    """

    groups = get_ingredient_item_groups_for_recipe(recipe_id=recipe_id)
    data = parse_obj_as(list[RecipeIngredientGroupsListOut], groups)

    return APIResponse(status="success", data=data)
