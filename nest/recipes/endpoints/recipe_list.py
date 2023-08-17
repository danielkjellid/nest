from django.http import HttpRequest
from ninja import Schema
from datetime import timedelta
from decimal import Decimal
from nest.api.responses import APIResponse
from ..selectors import get_recipes

from .router import router


class RecipeListOut(Schema):
    id: int


@router.get("/", response=APIResponse[list[RecipeListOut]])
def recipe_list_api(request: HttpRequest) -> APIResponse[list[RecipeListOut]]:
    """
    Get a list of all recipes in the application.
    """

    recipes = get_recipes()

    return APIResponse(status="success", data=recipes)
