from django.http import HttpRequest
from ninja import Router, Schema
from store_kit.http import status

from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.core.fields import FormField

from .forms import IngredientCreateForm
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


class IngredientListProductOut(Schema):
    id: int
    full_name: str
    thumbnail_url: str | None


class IngredientListOut(Schema):
    id: int
    title: str
    product: IngredientListProductOut


@router.get("/", response=APIResponse[list[IngredientListOut]])
def recipe_ingredient_list_api(
    request: HttpRequest,
) -> APIResponse[list[IngredientListOut]]:
    """
    Get a list off all ingredients in the application
    """

    ingredients = get_recipe_ingredients()
    data = [IngredientListOut(**ingredient.dict()) for ingredient in ingredients]

    return APIResponse(status="success", data=data)


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


class RecipeIngredientGroupsListIngredientProductOut(Schema):
    full_name: str
    thumbnail_url: str | None


class RecipeIngredientGroupsListIngredientOut(Schema):
    id: int
    title: str
    product: RecipeIngredientGroupsListIngredientProductOut


class RecipeIngredientGroupsListItemPortionQuantityUnitOut(Schema):
    abbreviation: str


class RecipeIngredientGroupsListItemOut(Schema):
    id: int
    ingredient: RecipeIngredientGroupsListIngredientOut
    portion_quantity_unit: RecipeIngredientGroupsListItemPortionQuantityUnitOut


class RecipeIngredientGroupsListOut(Schema):
    id: int
    title: str
    ingredient_items: list[RecipeIngredientGroupsListItemOut]


@router.get(
    "{recipe_id}/groups/",
    response=APIResponse[list[RecipeIngredientGroupsListOut]],
)
@staff_required
def recipe_ingredient_groups_list_api(
    request: HttpRequest, recipe_id: int
) -> APIResponse[list[RecipeIngredientGroupsListOut]]:
    """
    Get a list of all RecipeIngredientItemGroups for a recipe.
    """

    groups = get_recipe_ingredient_item_groups_for_recipe(recipe_id=recipe_id)
    data = [RecipeIngredientGroupsListOut(**group.dict()) for group in groups]

    return APIResponse(status="success", data=data)
