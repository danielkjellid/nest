from django.http import HttpRequest
from ninja import Router

from nest.api.responses import APIResponse
from nest.recipes.plans.records import RecipePlanRecord
from nest.recipes.plans.selectors import get_recipe_plans_for_home

router = Router(tags=["Recipe plans"])


@router.get("/homes/{home_id}/", response=APIResponse[list[RecipePlanRecord]])
def recipe_plan_list_api(
    request: HttpRequest, home_id: int
) -> APIResponse[list[RecipePlanRecord]]:
    recipe_plans = get_recipe_plans_for_home(home_id=home_id)
    return APIResponse(status="success", data=recipe_plans)
