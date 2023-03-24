import json
from typing import Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class FrontendView(View):
    """
    A Frontend view is a view that renders/serves the vite frontend app.
    """

    base_template = "frontend.html"

    def get_initial_props(self, request: HttpRequest) -> dict[str, Any]:
        return {"test": 10}

    def get_context(self, request: HttpRequest) -> dict[str, Any]:
        return {
            "DJANGO_VITE_DEV_MODE": settings.DJANGO_VITE_DEV_MODE,
            "DJANGO_VITE_DEV_SERVER_HOST": settings.DJANGO_VITE_DEV_SERVER_HOST,
            "DJANGO_VITE_DEV_SERVER_PORT": settings.DJANGO_VITE_DEV_SERVER_PORT,
            "initial_props": json.dumps(self.get_initial_props(request), indent=4),
        }

    def get_base_template(self, request: HttpRequest) -> str:
        if not self.base_template:
            raise RuntimeError(f"A base template must be specified for {self}")
        return self.base_template

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context(request)
        base_template = self.get_base_template(request)
        return render(request, base_template, context)
