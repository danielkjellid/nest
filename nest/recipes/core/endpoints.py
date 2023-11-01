from decimal import Decimal

from django.http import HttpRequest
from ninja import Router, Schema
from pydantic import parse_obj_as

from nest.api import status
from nest.api.fields import FormField
from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.frontend.components import FrontendComponents

from .enums import RecipeDifficulty, RecipeStatus
from .selectors import get_recipe, get_recipes
from .services import create_recipe

router = Router(tags=["Recipe"])


class RecipeCreateIn(Schema):
    title: str = FormField(..., order=1, help_text="Name of the recipe.")
    search_keywords: str | None = FormField(
        None, order=2, help_text="Separate with spaces. Title is included by default."
    )
    default_num_portions: str = FormField(
        ...,
        default_value=4,
        order=3,
        component=FrontendComponents.COUNTER.value,
        min=1,
        max=10,
        col_span=4,
    )
    status: RecipeStatus | str = FormField(..., order=4, col_span=2)
    difficulty: RecipeDifficulty | str = FormField(..., order=5, col_span=2)
    external_id: str | None = FormField(
        None, order=6, help_text="Providers identifier.", col_span=1
    )
    external_url: str | None = FormField(
        None,
        order=7,
        help_text="Direct link to the recipe on a provider's site",
        col_span=3,
    )
    is_vegetarian: bool = FormField(
        False,
        help_text="The recipe does not conatin any meat or fish products.",
        order=9,
    )
    is_pescatarian: bool = FormField(
        False, help_text="The recipe contains fish.", order=10
    )

    class FormMeta:
        columns = 4


class RecipeCreateOut(Schema):
    recipe_id: int


@router.post("create/", response={201: APIResponse[RecipeCreateOut]})
@staff_required
def recipe_create_api(
    request: HttpRequest, payload: RecipeCreateIn
) -> tuple[int, APIResponse[RecipeCreateOut]]:
    """
    Create a recipe.
    """
    recipe = create_recipe(**payload.dict(), request=request)
    return status.HTTP_201_CREATED, APIResponse(
        status="success", data=RecipeCreateOut(recipe_id=recipe.id)
    )


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
    status: RecipeStatus
    status_display: str
    difficulty_display: str
    is_vegetarian: bool
    is_pescatarian: bool
    duration: RecipeDetailDurationOut
    steps: list[RecipeDetailStepOut]
    ingredient_groups: list[RecipeDetailIngredientGroupOut]


@router.get("/recipe/{recipe_id}/", response=APIResponse[RecipeDetailOut], auth=None)
def recipe_detail_api(
    request: HttpRequest, recipe_id: int
) -> APIResponse[RecipeDetailOut]:
    """
    Retrieve a single recipe instance based in recipe id.
    """
    recipe = get_recipe(pk=recipe_id)
    return APIResponse(status="success", data=RecipeDetailOut(**recipe.dict()))


class RecipeListOut(Schema):
    id: int
    title: str
    default_num_portions: int
    status_display: str
    difficulty_display: str
    is_vegetarian: bool
    is_pescatarian: bool


@router.get("/", response=APIResponse[list[RecipeListOut]])
def recipe_list_api(request: HttpRequest) -> APIResponse[list[RecipeListOut]]:
    """
    Get a list of all recipes in the application.
    """
    recipes = get_recipes()
    data = parse_obj_as(list[RecipeListOut], recipes)

    return APIResponse(status="success", data=data)
