from django.http import HttpRequest
from ninja import Router, Schema
from store_kit.http import status

from nest.api.responses import APIResponse
from nest.core.decorators import staff_required

from .forms import IngredientCreateForm
from .records import RecipeIngredientRecord
from .selectors import (
    get_recipe_ingredients,
)
from .services import (
    create_recipe_ingredient,
    delete_recipe_ingredient,
)

router = Router(tags=["Recipe ingredients"])


@router.post("create/", response={201: APIResponse[None]})
@staff_required
def recipe_ingredient_create_api(
    request: HttpRequest, payload: IngredientCreateForm
) -> tuple[int, APIResponse[None]]:
    """
    Create an ingredient.
    """

    create_recipe_ingredient(**payload.dict(), request=request)
    return status.HTTP_201_CREATED, APIResponse(status="success", data=None)


class IngredientDeleteIn(Schema):
    ingredient_id: int


@router.delete("delete/", response=APIResponse[None])
@staff_required
def recipe_ingredient_delete_api(
    request: HttpRequest, payload: IngredientDeleteIn
) -> APIResponse[None]:
    """
    Delete an ingredient.
    """

    delete_recipe_ingredient(pk=payload.ingredient_id, request=request)
    return APIResponse(status="success", data=None)


@router.get("/", response=APIResponse[list[RecipeIngredientRecord]])
def recipe_ingredient_list_api(
    request: HttpRequest,
) -> APIResponse[list[RecipeIngredientRecord]]:
    """
    Get a list off all ingredients in the application
    """

    ingredients = get_recipe_ingredients()
    return APIResponse(status="success", data=ingredients)
