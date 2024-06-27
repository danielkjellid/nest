from django.db import transaction
from django.http import HttpRequest
from ninja import Router, Schema
from store_kit.http import status

from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.recipes.ingredients.services import (
    IngredientGroupItem,
)

from ..steps.services import Step
from .forms import RecipeCreateForm
from .records import RecipeDetailRecord
from .selectors import get_recipe, get_recipes
from .services import create_recipe, edit_recipe

router = Router(tags=["Recipe"])


class RecipeCreateIn(Schema):
    base_recipe: RecipeCreateForm
    ingredient_item_groups: list[IngredientGroupItem]
    steps: list[Step]


@router.post("create/", response={201: APIResponse[None]})
@staff_required
@transaction.atomic
def recipe_create_api(
    request: HttpRequest, payload: RecipeCreateIn
) -> tuple[int, APIResponse[None]]:
    """
    Create a full recipe instance.
    """
    base_recipe = payload.base_recipe
    create_recipe(
        title=base_recipe.title,
        search_keywords=base_recipe.search_keywords,
        status=base_recipe.status,
        difficulty=base_recipe.difficulty,
        default_num_portions=base_recipe.default_num_portions,
        external_id=base_recipe.external_id,
        external_url=base_recipe.external_url,
        is_vegetarian=base_recipe.is_vegetarian,
        is_pescatarian=base_recipe.is_pescatarian,
        ingredient_group_items=payload.ingredient_item_groups,
        steps=payload.steps,
        request=request,
    )

    return status.HTTP_201_CREATED, APIResponse(status="success", data=None)


class RecipeEditIn(Schema):
    base_recipe: RecipeCreateForm
    ingredient_item_groups: list[IngredientGroupItem] | None = None
    steps: list[Step] | None = None


@router.put("/recipe/{recipe_id}/", response=APIResponse[None])
@staff_required
def recipe_edit_api(
    request: HttpRequest, recipe_id: int, payload: RecipeEditIn
) -> APIResponse[None]:
    edit_recipe(
        recipe_id=recipe_id,
        base_edits=payload.base_recipe.dict(),
        ingredient_group_items=payload.ingredient_item_groups,
        steps=payload.steps,
        request=request,
    )
    return APIResponse(status="success", data=None)


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


@router.get("/", response=APIResponse[list[RecipeDetailRecord]])
def recipe_list_api(request: HttpRequest) -> APIResponse[list[RecipeDetailRecord]]:
    """
    Get a list of all recipes in the application.
    """
    recipes = get_recipes()
    return APIResponse(status="success", data=recipes)
