from ninja import Schema
from .router import router
from django.http import HttpRequest
from nest.selectors import UserSelector
from nest.api.responses import APIResponse
from nest.exceptions import ApplicationError


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
def user_list_api(request: HttpRequest):
    users = UserSelector.all_users()
    data = [UserList(**user.dict()) for user in users]

    return APIResponse(status="success", data=data)
