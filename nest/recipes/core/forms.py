from nest.forms.form import Form
from nest.api.fields import FormField
from .enums import RecipeStatus


class TestForm(Form):
    COLUMNS = 2

    id: int = FormField(..., order=1)
    name: str = FormField(..., max_length=3, order=3)

    status: RecipeStatus = FormField(..., order=2)
