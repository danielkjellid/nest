from django.http import HttpRequest, HttpResponse

from nest.core.exceptions import ApplicationError
from nest.products.endpoints import products_router
from nest.users.endpoints import users_router

from .base import NestAPI
from .responses import APIResponse

api = NestAPI()

api.add_router("/products/", products_router)
api.add_router("/users/", users_router)


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
