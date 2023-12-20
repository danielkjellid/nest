from django.http import HttpRequest
from ninja import Router, Schema
from store_kit.http import status

from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.core.fields import FormField

from .forms import IngredientCreateForm
from .records import RecipeIngredientItemGroupRecord, RecipeIngredientRecord
from .selectors import (
    get_recipe_ingredient_item_groups_for_recipe,
    get_recipe_ingredients,
)
from .services import (
    create_recipe_ingredient,
    create_recipe_ingredient_item_groups,
    delete_recipe_ingredient,
)

router = Router(tags=["Recipe ingredients"])


@router.post("create/", response={201: APIResponse[None]})
@staff_required
def recipe_ingredient_create_api(
    request: HttpRequest, payload: IngredientCreateForm
) -> tuple[int, APIResponse[None]]:
    """
    Create an ingredient.
    """

    create_recipe_ingredient(**payload.dict(), request=request)
    return status.HTTP_201_CREATED, APIResponse(status="success", data=None)


class IngredientDeleteIn(Schema):
    ingredient_id: int


@router.delete("delete/", response=APIResponse[None])
@staff_required
def recipe_ingredient_delete_api(
    request: HttpRequest, payload: IngredientDeleteIn
) -> APIResponse[None]:
    """
    Delete an ingredient.
    """

    delete_recipe_ingredient(pk=payload.ingredient_id, request=request)
    return APIResponse(status="success", data=None)


@router.get("/", response=APIResponse[list[RecipeIngredientRecord]])
def recipe_ingredient_list_api(
    request: HttpRequest,
) -> APIResponse[list[RecipeIngredientRecord]]:
    """
    Get a list off all ingredients in the application
    """

    ingredients = get_recipe_ingredients()
    return APIResponse(status="success", data=ingredients)


class RecipeIngredientsCreateIngredientIn(Schema):
    ingredient_id: str = FormField(..., alias="ingredient")
    portion_quantity: str
    portion_quantity_unit_id: str = FormField(..., alias="unit")
    additional_info: str | None


class RecipeIngredientsCreateIn(Schema):
    title: str
    ordering: int
    ingredients: list[RecipeIngredientsCreateIngredientIn]


@router.post("{recipe_id}/groups/create/", response={201: APIResponse[None]})
@staff_required
def recipe_ingredient_groups_create_api(
    request: HttpRequest, recipe_id: int, payload: list[RecipeIngredientsCreateIn]
) -> tuple[int, APIResponse[None]]:
    """
    Add ingredients to an existing recipe.
    """
    create_recipe_ingredient_item_groups(
        recipe_id=recipe_id,
        ingredient_group_items=[p.dict() for p in payload],
    )
    return status.HTTP_201_CREATED, APIResponse(status="success", data=None)


@router.get(
    "{recipe_id}/groups/",
    response=APIResponse[list[RecipeIngredientItemGroupRecord]],
)
@staff_required
def recipe_ingredient_groups_list_api(
    request: HttpRequest, recipe_id: int
) -> APIResponse[list[RecipeIngredientItemGroupRecord]]:
    """
    Get a list of all RecipeIngredientItemGroups for a recipe.
    """

    groups = get_recipe_ingredient_item_groups_for_recipe(recipe_id=recipe_id)
    return APIResponse(status="success", data=groups)
