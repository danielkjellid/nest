from typing import Any
from nest.models import User
from hijack import signals
from django.http import HttpRequest
import structlog

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
