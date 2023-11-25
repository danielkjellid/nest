from typing import ClassVar

from nest.forms.fields import FormField
from nest.frontend.components import FrontendComponents
from nest.api.openapi import form
from pydantic import BaseModel
from .enums import RecipeDifficulty, RecipeStatus


@form
class RecipeCreateForm(BaseModel):
    COLUMNS: ClassVar[int] = 4

    title: str = FormField(..., order=1, help_text="Name of the recipe.")
    search_keywords: str | None = FormField(
        None, order=2, help_text="Separate with spaces. Title is included by default."
    )
    default_num_portions: int = FormField(
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
        help_text="The recipe does not contain any meat or fish products.",
        order=9,
    )
    is_pescatarian: bool = FormField(
        False, help_text="The recipe contains fish.", order=10
    )
