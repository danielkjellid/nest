from django.http import HttpRequest, HttpResponse

from .responses import APIResponse
from nest.exceptions import ApplicationError
from .base import NestAPI
from nest.endpoints.users import router
from nest.endpoints.example import router as example_router

api = NestAPI()

api.add_router("/users/", router)
api.add_router("/example/", example_router)


@api.exception_handler(ApplicationError)
def application_error_handler(
    request: HttpRequest, exc: ApplicationError
) -> HttpResponse:

    """
    Exception handler for application errors.
    """

    return api.create_response(
        request,
        APIResponse(status="error", message=exc.message, data=exc.extra or None),
        status=exc.status_code,
    )
