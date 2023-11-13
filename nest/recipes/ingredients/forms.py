from nest.forms.fields import FormField
from nest.forms.models import Form
from nest.frontend.components import FrontendComponents


class IngredientCreateForm(Form):
    title: str = FormField(
        ..., order=1, help_text="User friendly title. E.g. Red tomatoes."
    )
    product_id: int = FormField(
        ..., alias="product", order=2, component=FrontendComponents.SELECT.value
    )
