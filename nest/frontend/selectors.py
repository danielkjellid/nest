from django.conf import settings
from django.http import HttpRequest

from nest.frontend.records import (
    CoreConfigRecord,
    CoreInitialPropsRecord,
    CoreMenuItemRecord,
)
from nest.homes.selectors import HomeSelector
from nest.users.records import UserRecord

from .menu import MENU


class CoreSelector:
    @classmethod
    def initial_props(cls, request: HttpRequest) -> CoreInitialPropsRecord | None:
        """
        Create a structure for passing down initial props on page load.
        """

        # Props content is largely based on a request user context.
        if not request.user or not request.user.is_authenticated:
            return None

        user = UserRecord.from_user(user=request.user)
        menu = cls.user_menu(user=user)
        available_homes = HomeSelector.user_homes(user=user)

        return CoreInitialPropsRecord(
            menu=menu,
            config=CoreConfigRecord(is_production=settings.IS_PRODUCTION),
            current_user=user,
            available_homes=available_homes,
        )

    @classmethod
    def user_menu(cls, user: UserRecord) -> list[CoreMenuItemRecord]:
        """
        Get the menu items for a specific user based on provided record.
        """

        # If a user is staff, pass all menu items without filtering.
        if user.is_staff or user.is_superuser:
            return [CoreMenuItemRecord(**item.dict()) for item in MENU]

        # Filter out admin items for "normal" users.
        return [
            CoreMenuItemRecord(**item.dict()) for item in MENU if not item.require_admin
        ]
