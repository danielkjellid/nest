from .base import NestForms
from nest.recipes.forms import forms as recipe_forms

forms = NestForms()

forms.add_forms(recipe_forms)
