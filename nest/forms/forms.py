from nest.products.forms import forms as product_forms
from nest.recipes.forms import forms as recipe_forms
from nest.users.forms import forms as users_forms

from .base import NestForms

forms = NestForms()

forms.add_forms(product_forms)
forms.add_forms(recipe_forms)
forms.add_forms(users_forms)
