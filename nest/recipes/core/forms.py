from nest.forms.form import Form
from .enums import RecipeStatus


class TestForm(Form):
    COLUMNS = 2

    id: int
    name: str
    status: RecipeStatus
