from .router import router
from django.http import HttpRequest
from ninja import Schema
from nest.api.responses import APIResponse
from ..services import create_recipe_steps
from nest.core.decorators import staff_required


class RecipeStepsCreateIn(Schema):
    number: int
    duration: int
    instruction: str
    step_type: str
    ingredient_items: list[str]


@router.post("{recipe_id}/steps/create/", response=APIResponse[None])
@staff_required
def recipe_steps_create_api(
    request: HttpRequest, recipe_id: int, payload: list[RecipeStepsCreateIn]
) -> APIResponse[None]:
    """
    Create steps related to a single recipe.
    """
    create_recipe_steps(recipe_id=recipe_id, steps=[p.dict() for p in payload])
    return APIResponse(status="success", data=None)