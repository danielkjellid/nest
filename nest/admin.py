from typing import TypeVar

from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.db.models import Model as DjangoModel

models = apps.get_models()

M = TypeVar("M", bound=DjangoModel)
A = TypeVar("A", bound=AdminSite)


class ListAdminMixin:
    def __init__(self, django_model: M, admin_site: A) -> None:
        try:
            self.list_display = django_model.ADMIN_LIST_DISPLAY  # type: ignore
        except AttributeError:
            self.list_display = [field.name for field in django_model._meta.fields]

        super().__init__(django_model, admin_site)  # type: ignore


for model in models:
    admin_class = type("AdminClass", (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
