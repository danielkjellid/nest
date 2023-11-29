from django.conf import settings
from django.http import HttpRequest

from nest.frontend.records import (
    FrontendConfigRecord,
    FrontendInitialPropsRecord,
    FrontendMenuItemRecord,
)
from nest.homes.selectors import get_homes_for_user
from nest.users.core.types import User

from .menu import MENU


def get_initial_props(*, request: HttpRequest) -> FrontendInitialPropsRecord | None:
    """
    Create a structure for passing down initial props on page load.
    """

    # Props content is largely based on a request user context.
    if not request.user or not request.user.is_authenticated:
        return None

    user = User.from_user(user=request.user)
    menu = get_menu_for_user(user=user)
    available_homes = get_homes_for_user(user=user)

    return FrontendInitialPropsRecord(
        menu=menu,
        config=FrontendConfigRecord(is_production=settings.IS_PRODUCTION),
        current_user=user,
        available_homes=available_homes,
    )


def get_menu_for_user(*, user: User) -> list[FrontendMenuItemRecord]:
    """
    Get the menu items for a specific user based on provided record.
    """

    # If a user is staff, pass all menu items without filtering.
    if user.is_staff or user.is_superuser:
        return [FrontendMenuItemRecord(**item.dict()) for item in MENU]

    # Filter out admin items for "normal" users.
    return [
        FrontendMenuItemRecord(**item.dict()) for item in MENU if not item.require_admin
    ]
