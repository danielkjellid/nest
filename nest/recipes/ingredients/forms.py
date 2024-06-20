from typing import ClassVar

from pydantic import BaseModel

from nest.api.openapi import form
from nest.core.fields import FormField
from nest.frontend.components import FrontendComponents


@form
class IngredientCreateForm(BaseModel):
    COLUMNS: ClassVar[int] = 1

    title: str = FormField(
        ..., order=1, help_text="User friendly title. E.g. Red tomatoes."
    )
    product_id: str | None = FormField(
        None,
        alias="product",
        order=2,
        component=FrontendComponents.SELECT.value,
    )
    is_base_ingredient: bool = FormField(
        False,
        order=3,
        help_text=(
            "The ingredient is something we expect users to already have available. "
            "E.g. salt."
        ),
    )
