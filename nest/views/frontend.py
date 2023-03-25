import json
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest

from .base import ReactView


class FrontendView(LoginRequiredMixin, ReactView):
    template_name = "frontend.html"
    frontend_app = "frontend/apps/index.tsx"

    @staticmethod
    def get_initial_props(request: HttpRequest) -> dict[str, Any]:
        return {"test": 11}

    def get_additional_context(self, request: HttpRequest) -> dict[str, Any]:
        return {"initial_props": json.dumps(self.get_initial_props(request), indent=4)}
