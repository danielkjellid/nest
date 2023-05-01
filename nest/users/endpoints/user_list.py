from django.http import HttpRequest
from ninja import Schema

from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.users.selectors import get_users

from .router import router


class UserListHomeOut(Schema):
    id: int
    address: str
    is_active: bool


class UserListOut(Schema):
    id: int
    email: str
    full_name: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    home: UserListHomeOut | None


@router.get("/", response=APIResponse[list[UserListOut]])
@staff_required
def user_list_api(request: HttpRequest) -> APIResponse[list[UserListOut]]:
    """
    Get a list of all users in the application.
    """

    users = get_users()
    data = [UserListOut(**user.dict()) for user in users]

    return APIResponse(status="success", data=data)
