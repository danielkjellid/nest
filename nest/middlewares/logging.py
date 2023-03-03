from typing import Callable

from django.http import HttpRequest

import structlog

logger = structlog.get_logger(__name__)


class GenericLoggingMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], None]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> None:
        logger.new(path=request.path, method=request.method)

        if hasattr(request, "user"):
            logger.bind(user_id=request.user.id)

        if hasattr(request, "auth"):
            logger.bind(user_id=request.auth.id)  # type: ignore

        return self.get_response(request)
