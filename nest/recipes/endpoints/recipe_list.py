from django.http import HttpRequest
from ninja import Schema

from nest.api.responses import APIResponse
from ..selectors import get_recipes

from .router import router


class RecipeListIngredientProductOut(Schema):
    full_name: str
    thumbnail_url: str | None


class RecipeListIngredientOut(Schema):
    id: int
    title: str
    product: RecipeListIngredientProductOut


class RecipeListIngredientItemPortionUnitOut(Schema):
    abbreviation: str


class RecipeListIngredientItemOut(Schema):
    id: int
    ingredient: RecipeListIngredientOut
    portion_quantity_display: str
    portion_quantity_unit: RecipeListIngredientItemPortionUnitOut


class RecipeListIngredientItemGroupOut(Schema):
    id: int
    title: str
    ingredient_items: list[RecipeListIngredientItemOut]


class RecipeListOut(Schema):
    id: int
    title: str
    default_num_portions: int
    ingredient_item_groups: list[RecipeListIngredientItemGroupOut]


@router.get("/", response=APIResponse[list[RecipeListOut]])
def recipe_list_api(request: HttpRequest) -> APIResponse[list[RecipeListOut]]:
    """
    Get a list of all recipes in the application.
    """

    recipes = get_recipes()

    return APIResponse(status="success", data=recipes)
