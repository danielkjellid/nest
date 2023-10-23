from ninja import Schema
from .router import router
from nest.api.responses import APIResponse
from django.http import HttpRequest
from ..selectors import get_recipe
from ..records import RecipeDetailRecord
from decimal import Decimal


class RecipeDetailDurationOut(Schema):
    preparation_time_iso8601: str
    cooking_time_iso8601: str
    total_time_iso8601: str


class RecipeDetailIngredientItemGroupOut(Schema):
    id: int


class RecipeDetailIngredientOut(Schema):
    id: int
    title: str


class RecipeDetailIngredientItemUnitOut(Schema):
    abbreviation: str


class RecipeDetailIngredientItemOut(Schema):
    id: int
    ingredient: RecipeDetailIngredientOut
    portion_quantity: Decimal
    portion_quantity_display: str
    portion_quantity_unit: RecipeDetailIngredientItemUnitOut


class RecipeDetailStepOut(Schema):
    id: int
    number: int
    instruction: str
    step_type_display: str
    ingredient_items: list[RecipeDetailIngredientItemOut]


class RecipeDetailIngredientGroupOut(Schema):
    id: int
    title: str
    ingredient_items: list[RecipeDetailIngredientItemOut]


class RecipeDetailOut(Schema):
    id: int
    title: str
    slug: str
    default_num_portions: int
    search_keywords: str | None
    external_id: str | None
    external_url: str | None
    status_display: str
    difficulty_display: str
    is_vegetarian: bool
    is_pescatarian: bool
    duration: RecipeDetailDurationOut
    steps: list[RecipeDetailStepOut]
    ingredient_groups: list[RecipeDetailIngredientGroupOut]


@router.get("{recipe_id}/", response=APIResponse[RecipeDetailOut])
def recipe_detail_api(
    request: HttpRequest, recipe_id: int
) -> APIResponse[RecipeDetailOut]:
    """
    Retrieve a single recipe instance based in recipe id.
    """
    recipe = get_recipe(pk=recipe_id)
    return APIResponse(status="success", data=RecipeDetailOut(**recipe.dict()))
