import json
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpRequest

from nest.core.utils.humps import HumpsUtil

from ..selectors import CoreSelector
from .base import ReactView


class FrontendView(LoginRequiredMixin, ReactView):
    template_name = "frontend.html"
    frontend_app = "frontend/index.tsx"

    def get_additional_context(self, request: HttpRequest) -> dict[str, Any]:
        props = CoreSelector.initial_props(request=request)

        return {
            "initial_props": json.dumps(
                HumpsUtil.camelize(props.dict()) if props else {},
                indent=4,
                cls=DjangoJSONEncoder,
            )
        }
