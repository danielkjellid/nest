from django.http import HttpRequest
from ninja import Router, Schema
from store_kit.http import status

from nest.api.responses import APIResponse
from nest.core.decorators import staff_required

from .forms import RecipeCreateForm
from .records import RecipeDetailRecord, RecipeRecord
from .selectors import get_recipe, get_recipes
from .services import create_recipe

router = Router(tags=["Recipe"])


class RecipeCreateOut(Schema):
    recipe_id: int


@router.post("create/", response={201: APIResponse[RecipeCreateOut]})
@staff_required
def recipe_create_api(
    request: HttpRequest, payload: RecipeCreateForm
) -> tuple[int, APIResponse[RecipeCreateOut]]:
    """
    Create a recipe.
    """
    recipe = create_recipe(**payload.dict(), request=request)
    return status.HTTP_201_CREATED, APIResponse(
        status="success", data=RecipeCreateOut(recipe_id=recipe.id)
    )


@router.get(
    "/recipe/{recipe_id}/",
    response=APIResponse[RecipeDetailRecord],
    auth=None,
)
def recipe_detail_api(
    request: HttpRequest, recipe_id: int
) -> APIResponse[RecipeDetailRecord]:
    """
    Retrieve a single recipe instance based in recipe id.
    """
    recipe = get_recipe(pk=recipe_id)
    return APIResponse(status="success", data=recipe)


@router.get("/", response=APIResponse[list[RecipeRecord]])
def recipe_list_api(request: HttpRequest) -> APIResponse[list[RecipeRecord]]:
    """
    Get a list of all recipes in the application.
    """
    recipes = get_recipes()
    return APIResponse(status="success", data=recipes)
