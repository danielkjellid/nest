from django.http import HttpRequest
from ninja import Schema
from nest.api.responses import APIResponse
from .router import router
from nest.services import UserService
from nest.decorators import staff_required


class UsersToggleActive(Schema):
    user_ids: list[int]


@router.post("toggle-active/", response=APIResponse[None])
@staff_required
def users_toggle_active_api(
    request: HttpRequest, payload: UsersToggleActive
) -> APIResponse[None]:
    """
    Toggle a single user's, or a list of users', active state.
    """
    UserService.toggle_active(user_ids=payload.user_ids)

    return APIResponse(
        status="success",
        message="Users successfully updated.",
        data=None,
    )
