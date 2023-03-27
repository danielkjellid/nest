from django.contrib import admin
from django.urls import include, path, re_path

from nest.views import FrontendView, LoginView
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("", FrontendView.as_view(), name="index"),
]


if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
