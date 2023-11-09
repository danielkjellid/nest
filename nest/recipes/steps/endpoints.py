from django.http import HttpRequest
from ninja import Router, Schema
from store_kit.http import status

from nest.api.responses import APIResponse
from nest.core.decorators import staff_required

from .services import create_recipe_steps

router = Router(tags=["Recipe steps"])


class RecipeStepsCreateIn(Schema):
    number: int
    duration: int
    instruction: str
    step_type: str
    ingredient_items: list[str]  # Ids


@router.post("{recipe_id}/create/", response={201: APIResponse[None]})
@staff_required
def recipe_steps_create_api(
    request: HttpRequest, recipe_id: int, payload: list[RecipeStepsCreateIn]
) -> tuple[int, APIResponse[None]]:
    """
    Create steps related to a single recipe.
    """
    create_recipe_steps(
        recipe_id=recipe_id,
        steps=[p.dict() for p in payload],
    )
    return status.HTTP_201_CREATED, APIResponse(status="success", data=None)
