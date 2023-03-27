from django.http import HttpRequest
from pydantic import BaseModel

from nest.menu import MENU
from nest.records import (
    CoreConfigRecord,
    CoreInitialPropsRecord,
    CoreMenuItemRecord,
    UserRecord,
)

from .homes import HomeSelector
from .users import UserSelector


class MenuItem(BaseModel):
    key: str
    title: str
    end: bool


class CoreSelector:
    ...

    @classmethod
    def initial_props(cls, request: HttpRequest) -> CoreInitialPropsRecord | None:

        if not request.user or not request.user.is_authenticated:
            return None

        user = request.user
        menu = cls.menu_for_user(user_id=user.id)
        user_record = UserRecord.from_user(user=user)
        available_homes = HomeSelector.for_user(user_id=user.id)

        return CoreInitialPropsRecord(
            menu=menu,
            config=CoreConfigRecord(is_production=False),
            current_user=user_record,
            available_homes=available_homes,
        )

    @classmethod
    def menu_for_user(cls, user_id: int) -> list[CoreMenuItemRecord]:
        user = UserSelector.get_user(pk=user_id)

        if user.is_staff:
            return [CoreMenuItemRecord(**item.dict()) for item in MENU]

        # Filter out admin items.
        return [
            CoreMenuItemRecord(**item.dict()) for item in MENU if not item.require_admin
        ]
