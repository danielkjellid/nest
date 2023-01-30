import time

import structlog
from asgi_correlation_id import correlation_id
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from uvicorn.protocols.utils import get_path_with_query_string
from typing import Any, Callable
from nest import config
from nest.logging_utils import setup_logging

setup_logging(json_logs=False, log_level=config.LOG_LEVEL)  # TODO: Fix json logs bool

access_logger = structlog.stdlib.get_logger("api.access")


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to initialize logging,
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[..., Any]
    ) -> Response:
        structlog.contextvars.clear_contextvars()
        request_id = correlation_id.get()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        start_time = time.perf_counter_ns()

        # If the call_next raises an error, we still want to return our own 500 response,
        # so we can add headers to it (process time, request ID...)
        response = Response(status_code=500)

        try:
            response = await call_next(request)
        except Exception:
            structlog.stdlib.get_logger("api.error").exception("Uncaught exception")
            raise
        finally:
            process_time = time.perf_counter_ns() - start_time
            status_code = response.status_code
            url = get_path_with_query_string(request.scope)
            client_host = getattr(request.client, "host", None)
            client_port = getattr(request.client, "port", None)
            http_method = request.method
            http_version = request.scope["http_version"]
            # Recreate the Uvicorn access log format, but add all parameters as structured information
            access_logger.info(
                f"""{client_host}:{client_port} - "{http_method} {url} HTTP/{http_version}" {status_code}""",
                http={
                    "url": str(request.url),
                    "status_code": status_code,
                    "method": http_method,
                    "request_id": request_id,
                    "version": http_version,
                },
                network={"client": {"ip": client_host, "port": client_port}},
                duration=process_time,
            )
            response.headers["X-Process-Time"] = str(process_time / 10**9)
            return response  # noqa
