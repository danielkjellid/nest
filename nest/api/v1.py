from ninja import NinjaAPI
from django.contrib.admin.views.decorators import staff_member_required
from ninja.security import django_auth

from nest.endpoints.users import router

api = NinjaAPI(
    title="Nest API",
    version="1.0.0",
    docs_decorator=staff_member_required,
    auth=django_auth,
    csrf=True,
)

api.add_router("/users/", router)
