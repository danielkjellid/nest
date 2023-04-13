from django.conf import settings
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path, re_path

from nest.api.v1 import api as api_v1
from nest.frontend.views import FrontendView, LoginView

urlpatterns: list[URLPattern | URLResolver] = []

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

urlpatterns += [
    path("admin/", admin.site.urls),
    path("hijack/", include("hijack.urls")),
    path("login/", LoginView.as_view(), name="login"),
    path("api/v1/", api_v1.urls),
    re_path("", FrontendView.as_view(), name="index"),
]
