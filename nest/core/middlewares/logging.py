from typing import Callable

import structlog
from django.http import HttpRequest

logger = structlog.get_logger(__name__)


class GenericLoggingMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], None]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> None:
        logger.new(path=request.path, method=request.method)

        if hasattr(request, "user") and hasattr(request.user, "id"):
            logger.bind(user_id=request.user.id)

        if hasattr(request, "auth"):
            logger.bind(user_id=request.auth.id)

        return self.get_response(request)
