from django.http import HttpRequest
from ninja import Schema

from nest.api.responses import APIResponse

from ..selectors import get_ingredients
from .router import router


class IngredientListProductOut(Schema):
    id: int
    full_name: str
    thumbnail_url: str | None


class IngredientListOut(Schema):
    id: int
    title: str
    product: IngredientListProductOut


@router.get("/", response=APIResponse[list[IngredientListOut]])
def ingredient_list_api(request: HttpRequest) -> APIResponse[list[IngredientListOut]]:
    """
    Get a list off all ingredients in the application
    """

    ingredients = get_ingredients()
    data = [IngredientListOut(**ingredient.dict()) for ingredient in ingredients]

    return APIResponse(status="success", data=data)
