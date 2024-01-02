from django.http import HttpRequest
from ninja import Router, Schema
from store_kit.http import status

from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.core.fields import FormField

from .forms import RecipeCreateForm
from .records import RecipeDetailRecord, RecipeRecord
from .selectors import get_recipe, get_recipes
from .services import create_base_recipe, create_recipe

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
    recipe = create_base_recipe(**payload.dict(), request=request)
    return status.HTTP_201_CREATED, APIResponse(
        status="success", data=RecipeCreateOut(recipe_id=recipe.id)
    )


class RecipeCreateIngredientItem(Schema):
    ingredient_id: str = FormField(..., alias="ingredient")
    portion_quantity: str
    portion_quantity_unit_id: str = FormField(..., alias="portion_quantity_unit")
    additional_info: str | None


class RecipeCreateSteps(Schema):
    number: int
    duration: int
    instruction: str
    step_type: str
    ingredient_items: list[RecipeCreateIngredientItem]


class RecipeCreateIngredientItemGroup(Schema):
    title: str
    ordering: int
    ingredients: list[RecipeCreateIngredientItem]


class RecipeCreateIn(Schema):
    base_recipe: RecipeCreateForm
    steps: list[RecipeCreateSteps]
    ingredient_item_groups: list[RecipeCreateIngredientItemGroup]


@router.post("create2/", response={201: APIResponse[None]})
@staff_required
def recipe_create2_api(
    request: HttpRequest, payload: RecipeCreateIn
) -> tuple[int, APIResponse[None]]:
    """
    Create a full recipe instance.
    """
    base_recipe = payload.base_recipe.dict()
    ingredient_item_groups = [p.dict() for p in payload.ingredient_item_groups]
    steps = [p.dict() for p in payload.steps]

    create_recipe(
        **base_recipe,
        ingredient_group_items=ingredient_item_groups,
        steps=steps,
        request=request,
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
