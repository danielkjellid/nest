from django.http import HttpRequest
from ninja import Router

from nest.api.responses import APIResponse
from nest.core.decorators import staff_required

from .selectors import get_users
from .types import User

router = Router(tags=["Users"])


@router.get("/", response=APIResponse[list[User]])
@staff_required
def user_list_api(request: HttpRequest) -> APIResponse[list[User]]:
    """
    Get a list of all users in the application.
    """

    users = get_users()
    return APIResponse(status="success", data=users)
