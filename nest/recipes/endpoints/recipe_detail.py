from ninja import Schema
from .router import router
from nest.api.responses import APIResponse
from django.http import HttpRequest
from ..selectors import get_recipe
from ..records import RecipeDetailRecord


# class RecipeDetailDurationOut(Schema):
#     preparation_time_iso8601: str
#     cooking_time_iso8601: str
#     total_time_iso8601: str
#
#
# class RecipeDetailStepOut(Schema):
#     id: int
#     number: int
#     duration: str
#     instruction: str
#     # step_type: str
#
#
# class RecipeDetailOut(Schema):
#     id: int
#     title: str
#     default_num_portions: int
#     external_id: str | None
#     external_url: str | None
#     status_display: str
#     difficulty_display: str
#     is_vegetarian: bool
#     is_pescatarian: bool
#     duration: RecipeDetailDurationOut
#     steps: list[RecipeDetailStepOut]


@router.get("{recipe_id}/", response=APIResponse[RecipeDetailRecord])
def recipe_detail_api(
    request: HttpRequest, recipe_id: int
) -> APIResponse[RecipeDetailRecord]:
    """
    Retrieve a single recipe instance based in recipe id.
    """
    recipe = get_recipe(pk=recipe_id)
    return APIResponse(status="success", data=recipe)
