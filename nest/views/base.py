import json
from typing import Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class ReactView(View):
    """
    A React view is a view that renders/serves part of the vite frontend app.
    """

    template_name: str
    index_path: str

    def get_base_context(self) -> dict[str, Any]:
        return {
            "DJANGO_VITE_DEV_MODE": settings.DJANGO_VITE_DEV_MODE,
            "DJANGO_VITE_DEV_SERVER_HOST": settings.DJANGO_VITE_DEV_SERVER_HOST,
            "DJANGO_VITE_DEV_SERVER_PORT": settings.DJANGO_VITE_DEV_SERVER_PORT,
            "INDEX_PATH": self.index_path,
        }

    @staticmethod
    def get_additional_context(self, request: HttpRequest) -> dict[str, Any]:
        """
        Context to send to view. Should be implemented per class inheriting this class.
        """
        return {}

    def get_template(self, request: HttpRequest) -> str:
        """
        Template html to render.
        """
        if not self.template_name:
            raise RuntimeError(f"A template must be specified for {self}")
        return self.template_name

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = {**self.get_base_context(), **self.get_additional_context(request)}
        template = self.get_template(request)
        return render(request, template, context)
