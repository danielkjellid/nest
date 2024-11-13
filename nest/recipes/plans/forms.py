from typing import ClassVar

from pydantic import BaseModel

from nest.api.openapi import form
from nest.core.fields import FormField
from nest.frontend.components import FrontendComponents


@form
class RecipePlanCreateForm(BaseModel):
    COLUMNS: ClassVar[int] = 3

    budget: str = FormField(..., order=1, col_span=1)
    portions_per_recipe: int = FormField(
        ...,
        order=2,
        min=1,
        max=99,
        col_span=1,
        component=FrontendComponents.COUNTER.value,
    )
    recipes_amount: int = FormField(
        ...,
        order=3,
        min=1,
        max=10,
        col_span=1,
        component=FrontendComponents.COUNTER.value,
    )
