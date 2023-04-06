from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from nest.api import api_v1
from nest.views import FrontendView, LoginView

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))]
else:
    urlpatterns = []

urlpatterns += [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("api/v1/", api_v1.urls),
    re_path("", FrontendView.as_view(), name="index"),
]
