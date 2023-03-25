from typing import Any

from django.contrib.auth.views import LoginView as DjangoLoginView

from .base import ReactView


class LoginView(DjangoLoginView, ReactView):
    template_name = "login.html"
    frontend_app = "frontend/apps/login/index.tsx"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        django_view_context = super().get_context_data(**kwargs)
        react_view_context = self.get_base_context()

        context = {**django_view_context, **react_view_context}

        return context
