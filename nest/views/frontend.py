import json
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest

from .base import ReactView
from nest.selectors import CoreSelector
from nest.utils import HumpsUtil


class FrontendView(LoginRequiredMixin, ReactView):
    template_name = "frontend.html"
    frontend_app = "frontend/apps/index.tsx"

    def get_additional_context(self, request: HttpRequest) -> dict[str, Any]:
        props = CoreSelector.initial_props(request=request)

        return {
            "initial_props": json.dumps(
                HumpsUtil.camelize(props.dict()) if props else {}, indent=4
            )
        }
