from django.http import HttpRequest
from ninja import Schema

from nest.api.responses import APIResponse
from nest.core.decorators import staff_required

from ..services import delete_ingredient
from .router import router


class IngredientDeleteIn(Schema):
    ingredient_id: int


@router.delete("delete/", response=APIResponse[None])
@staff_required
def ingredient_delete_api(
    request: HttpRequest, payload: IngredientDeleteIn
) -> APIResponse[None]:
    """
    Delete an ingredient.
    """

    delete_ingredient(pk=payload.ingredient_id, request=request)
    return APIResponse(status="success", data=None)
