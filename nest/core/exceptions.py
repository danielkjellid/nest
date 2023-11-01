from typing import Any

from nest.api import status


class ApplicationError(Exception):
    def __init__(
        self,
        message: Any,
        extra: Any | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message)

        self.message = message
        self.extra = extra or {}
        self.status_code = status_code
