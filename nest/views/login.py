from typing import Any

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect

from .base import ReactView


class LoginView(UserPassesTestMixin, DjangoLoginView, ReactView):
    template_name = "login.html"
    frontend_app = "frontend/apps/login/index.tsx"

    def test_func(self) -> bool | None:
        """
        The login view should only be available to unauthenticated users.
        If it returns false, it will fire the handle_no_permission function
        that redirects the user.
        """
        if self.request.user.is_authenticated:
            return False
        return True

    def handle_no_permission(self) -> HttpResponsePermanentRedirect:  # type: ignore
        """
        Redirect authenticated users to front page.
        """
        return redirect("index", permanent=True)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        django_view_context = super().get_context_data(**kwargs)
        react_view_context = self.get_base_context()

        context = {**django_view_context, **react_view_context}

        return context
