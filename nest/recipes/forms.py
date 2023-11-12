from nest.forms import AppForms
from .core.forms import TestForm

forms = AppForms(app="recipes")

forms.register_form(TestForm)
