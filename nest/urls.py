from django.contrib import admin
from django.urls import include, path

from nest.views import FrontendView, LoginView

urlpatterns = [
    path("", FrontendView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]
