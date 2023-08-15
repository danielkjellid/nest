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
    is_partial_recipe: bool = FormField(
        False,
        help_text="Designates if the recipe can be considered a full meal.",
        order=8,
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


@router.post("create/", response=APIResponse[RecipeCreateOut])
@staff_required
def recipe_create_api(
    request: HttpRequest, payload: RecipeCreateIn
) -> APIResponse[RecipeCreateOut]:
    """
    Create a recipe.
    """
    print(payload)
    recipe_id = create_recipe(**payload.dict(), request=request)
    return APIResponse(status="success", data=RecipeCreateOut(recipe_id=recipe_id))
