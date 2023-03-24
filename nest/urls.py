from django.contrib import admin
from django.urls import path
from .views import FrontendView

urlpatterns = [
    path("test/", FrontendView.as_view(), name="index"),
    path("admin/", admin.site.urls),
]
