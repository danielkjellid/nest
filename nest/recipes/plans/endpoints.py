from decimal import Decimal

from django.http import HttpRequest
from django.utils import timezone
from ninja import Router

from nest.api.responses import APIResponse
from nest.recipes.plans.forms import RecipePlanCreateForm
from nest.recipes.plans.records import RecipePlanRecord
from nest.recipes.plans.selectors import get_recipe_plans_for_home
from nest.recipes.plans.services import create_recipe_plan

router = Router(tags=["Recipe plans"])


@router.get("/homes/{home_id}/", response=APIResponse[list[RecipePlanRecord]])
def recipe_plan_list_for_home_api(
    request: HttpRequest, home_id: int
) -> APIResponse[list[RecipePlanRecord]]:
    """
    Retrieve a list of plans related to a home.
    """
    recipe_plans = get_recipe_plans_for_home(home_id=home_id)
    return APIResponse(status="success", data=recipe_plans)


@router.post("/homes/{home_id}/", response=APIResponse[None])
def recipe_plan_create_for_home_api(
    request: HttpRequest, home_id: int, payload: RecipePlanCreateForm
) -> APIResponse[None]:
    create_recipe_plan(
        title=f"Ad-hoc plan {timezone.now()}",
        description="Plan created ad-hoc",
        from_date=timezone.now().date(),
        budget=Decimal(payload.budget),
        num_portions_per_recipe=payload.portions_per_recipe,
        num_items=payload.recipes_amount,
        num_pescatarian=0,
        num_vegetarian=0,
        home_id=home_id,
    )
    return APIResponse(status="success", data=None)
