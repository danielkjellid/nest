from django.contrib import admin
from django.urls import path

from nest.views import FrontendView, LoginView

urlpatterns = [
    path("", FrontendView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("admin/", admin.site.urls),
]
