from .base import ReactView
from typing import Any
from django.http import HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin
import json


class FrontendView(LoginRequiredMixin, ReactView):
    template_name = "frontend.html"
    index_path = "frontend/apps/index.tsx"

    def get_initial_props(self, request: HttpRequest) -> dict[str, Any]:
        return {"test": 11}

    def get_additional_context(self, request: HttpRequest) -> dict[str, Any]:
        return {"initial_props": json.dumps(self.get_initial_props(request), indent=4)}
