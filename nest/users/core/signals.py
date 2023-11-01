from typing import Any

import structlog
from django.http import HttpRequest
from hijack import signals

from .models import User

logger = structlog.getLogger()


def log_hijack_started(
    sender: Any, hijacker: User, hijacked: User, request: HttpRequest, **kwargs: Any
) -> None:
    logger.info(
        "Hijack session started",
        original_user=hijacker.id,
        hijacked_user=hijacked.id,
    )


signals.hijack_started.connect(log_hijack_started)


def log_hijack_ended(
    sender: Any, hijacker: User, hijacked: User, request: HttpRequest, **kwargs: Any
) -> None:
    logger.info(
        "Hijack session ended",
        original_user=hijacker.id,
        hijacked_user=hijacked.id,
    )


signals.hijack_ended.connect(log_hijack_ended)
