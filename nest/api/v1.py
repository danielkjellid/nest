from django.http import HttpRequest, HttpResponse

from .responses import APIResponse
from nest.exceptions import ApplicationError
from .base import NestAPI
from nest.endpoints import users_endpoints, example_endpoints

api = NestAPI()

api.add_router("/users/", users_endpoints)
api.add_router("/example/", example_endpoints)


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
