from django.http import HttpRequest
from ninja import Schema

from nest.api.responses import APIResponse
from nest.decorators import staff_required
from nest.selectors import UserSelector

from .router import router


class UserListHome(Schema):
    id: int
    address: str
    is_active: bool


class UserList(Schema):
    id: int
    email: str
    full_name: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    home: UserListHome | None


@router.get("/", response={200: APIResponse[list[UserList]]})
@staff_required
def users_list_api(request: HttpRequest) -> APIResponse[list[UserList]]:
    """
    Get a list of all users registered in the application.
    """
    users = UserSelector.all_users()
    data = [UserList(**user.dict()) for user in users]

    return APIResponse(status="success", data=data)
