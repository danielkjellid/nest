from django.http import HttpRequest
from ninja import File, Form, Schema

from nest.api.fields import FormField
from nest.api.files import UploadedFile
from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.recipes.enums import RecipeDifficulty, RecipeStatus
from nest.frontend.components import FrontendComponents
from nest.products.services import create_product

from .router import router


class RecipeCreateIn(Schema):
    title: str = FormField(..., order=1, help_text="Name of the recipe.")
    slug: str = FormField(..., order=2)
    search_keywords: str | None = FormField(
        None, order=3, help_text="Separate with spaces. Title is included by default."
    )
    default_num_portions: str = FormField(..., default_value=4, order=4)
    external_id: str | None = FormField(
        None, order=5, help_text="Recipe identifier on a provider's site."
    )
    external_url: str | None = FormField(
        None, order=6, help_text="Direct link to the recipe on a provider's site"
    )
    status: RecipeStatus
    difficulty: RecipeDifficulty
    is_partial_recipe: bool = FormField(
        False, help_text="Designates if the recipe can be considered a full meal."
    )
    is_vegetarian: bool = FormField(
        False, help_text="The recipe does not conatin any meat or fish products."
    )
    is_pescatarian: bool = FormField(False, help_text="The recipe contains fish.")


class RecipeCreateOut(Schema):
    recipe_id: int


@router.post("create/", response=APIResponse[RecipeCreateOut])
@staff_required
def recipe_create_api(
    request: HttpRequest, payload: RecipeCreateIn
) -> APIResponse[RecipeCreateOut]:
    """
    Create a recipe.
    """

    print(payload)
    return APIResponse(status="success", data=RecipeCreateOut(recipe_id=1))
