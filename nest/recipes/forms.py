from nest.forms.base import AppForms

from .core.forms import RecipeCreateForm
from .ingredients.forms import IngredientCreateForm

forms = AppForms(app="recipes")

forms.register_form(RecipeCreateForm)
forms.register_form(IngredientCreateForm)
