import json
from typing import Any

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpRequest

from nest.core.utils import camelize

from ..selectors import get_initial_props
from .base import ReactView


class RecipeView(ReactView):
    template_name = "recipe.html"
    frontend_app = "frontend/apps/recipe/index.tsx"

    def get_additional_context(self, request: HttpRequest) -> dict[str, Any]:
        props = get_initial_props(request=request)

        return {
            "initial_props": json.dumps(
                camelize(props.dict()) if props else {},
                indent=4,
                cls=DjangoJSONEncoder,
            )
        }
