from django.http import HttpRequest
from ninja import Router

from nest.api.responses import APIResponse
from nest.core.decorators import staff_required

from .records import UserRecord
from .selectors import get_users

router = Router(tags=["Users"])


@router.get("/", response=APIResponse[list[UserRecord]])
@staff_required
def user_list_api(request: HttpRequest) -> APIResponse[list[UserRecord]]:
    """
    Get a list of all users in the application.
    """

    users = get_users()
    return APIResponse(status="success", data=users)
