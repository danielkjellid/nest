from nest.forms.fields import FormField
from pydantic import BaseModel
from nest.frontend.components import FrontendComponents
from nest.api.openapi import form
from typing import ClassVar


@form
class IngredientCreateForm(BaseModel):
    COLUMNS: ClassVar[int] = 1

    title: str = FormField(
        ..., order=1, help_text="User friendly title. E.g. Red tomatoes."
    )
    product_id: int = FormField(
        ..., alias="product", order=2, component=FrontendComponents.SELECT.value
    )
