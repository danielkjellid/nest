from django.http import HttpRequest
from ninja import Schema

from nest.api.fields import FormField
from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.frontend.components import FrontendComponents
from ..services import create_ingredient
from .router import router


class IngredientCreateIn(Schema):
    title: str = FormField(
        ..., order=1, help_text="User friendly title. E.g. Red tomatoes."
    )
    product_id: int = FormField(
        ..., alias="product", order=2, component=FrontendComponents.SELECT.value
    )


@router.post("create/", response=APIResponse[None])
@staff_required
def ingredient_create_api(
    request: HttpRequest, payload: IngredientCreateIn
) -> APIResponse[None]:
    """
    Create an ingredient.
    """

    create_ingredient(**payload.dict(), request=request)
    return APIResponse(status="success", data=None)
