from django.apps import apps
from django.contrib import admin

models = apps.get_models()


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        try:
            self.list_display = model.Admin.list_display
        except AttributeError:
            self.list_display = [field.name for field in model._meta.fields]

        super(ListAdminMixin, self).__init__(model, admin_site)


for model in models:
    admin_class = type("AdminClass", (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
