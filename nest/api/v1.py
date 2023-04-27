from django.http import HttpRequest, HttpResponse
from ninja.errors import ValidationError as NinjaValidationError
from pydantic.error_wrappers import ValidationError as PydanticValidationError
from nest.core.exceptions import ApplicationError
from nest.products.endpoints import products_router
from nest.users.endpoints import users_router
from nest.units.endpoints import units_router
from nest.core.utils.humps import HumpsUtil
from .types import PydanticErrorDict
from typing import Any

from .base import NestAPI
from .responses import APIResponse

api = NestAPI()

api.add_router("/products/", products_router)
api.add_router("/units/", units_router)
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
        APIResponse(status="error", message=exc.message, data=exc.extra or None).dict(),
        status=exc.status_code,
    )


@api.exception_handler(NinjaValidationError)
@api.exception_handler(PydanticValidationError)
def models_validation_error(
    request: HttpRequest, exc: NinjaValidationError | PydanticValidationError
) -> HttpResponse:
    if isinstance(exc.errors, list):
        errors: list[PydanticErrorDict] = exc.errors
    else:
        errors: list[PydanticErrorDict] = exc.errors()

    field_errors: dict[str, Any] = {}

    for error in errors:
        location = error["loc"]
        field = HumpsUtil.camelize(location[len(location) - 1])
        field_errors[field] = error["msg"].capitalize()

    return api.create_response(
        request,
        APIResponse(
            status="error",
            message="There were some errors in the form.",
            data=field_errors,
        ).dict(),
        status=400,
    )
