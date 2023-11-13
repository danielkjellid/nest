from nest.forms.base import AppForms

from .core.forms import ProductCreateForm, ProductEditForm

forms = AppForms(app="products")

forms.register_form(ProductCreateForm)
forms.register_form(ProductEditForm)
