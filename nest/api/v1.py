from django.http import HttpRequest, HttpResponse

from nest.endpoints import products_endpoints, users_endpoints
from nest.exceptions import ApplicationError

from .base import NestAPI
from .responses import APIResponse

api = NestAPI()

api.add_router("/products/", products_endpoints)
api.add_router("/users/", users_endpoints)


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
