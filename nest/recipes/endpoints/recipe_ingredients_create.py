from django.http import HttpRequest
from ninja import File, Form, Schema

from nest.api.fields import FormField
from nest.api.files import UploadedFile
from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.recipes.enums import RecipeDifficulty, RecipeStatus
from nest.frontend.components import FrontendComponents
from nest.products.services import create_product
from nest.recipes.services import create_recipe

from .router import router


class RecipeIngredientsCreateIngredientIn(Schema):
    ingredient_id: str = FormField(..., alias="ingredient")
    amount: str
    unit_id: str = FormField(..., alias="unit")


class RecipeIngredientsCreateIn(Schema):
    title: str
    ingredients: list[RecipeIngredientsCreateIngredientIn]


@router.post("{recipe_id}/ingredients/create/", response=APIResponse[None])
@staff_required
def recipe_ingredients_create_api(
    request: HttpRequest, recipe_id: int, payload: list[RecipeIngredientsCreateIn]
) -> APIResponse[None]:
    """
    Add ingredients to an existing recipe.
    """
    print(recipe_id)
    print([p.dict() for p in payload])
    return APIResponse(status="success", data=None)
