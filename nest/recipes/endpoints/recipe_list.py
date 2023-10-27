from django.http import HttpRequest
from ninja import Schema
from pydantic import parse_obj_as

from nest.api.responses import APIResponse

from ..selectors import get_recipes
from .router import router


class RecipeListOut(Schema):
    id: int
    title: str
    default_num_portions: int
    status_display: str
    difficulty_display: str
    is_vegetarian: bool
    is_pescatarian: bool


@router.get("/", response=APIResponse[list[RecipeListOut]])
def recipe_list_api(request: HttpRequest) -> APIResponse[list[RecipeListOut]]:
    """
    Get a list of all recipes in the application.
    """
    recipes = get_recipes()
    data = parse_obj_as(list[RecipeListOut], recipes)

    return APIResponse(status="success", data=data)
