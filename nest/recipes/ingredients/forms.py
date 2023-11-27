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
    product_id: int = FormField(
        ..., alias="product", order=2, component=FrontendComponents.SELECT.value
    )
