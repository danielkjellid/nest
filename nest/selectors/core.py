from django.http import HttpRequest
from nest.records import (
    CoreInitialPropsRecord,
    UserRecord,
    CoreConfigRecord,
    CoreMenuItemRecord,
)
from nest.menu import MENU
from nest.models import User
from typing import Any
from pydantic import BaseModel
from nest.exceptions import ApplicationError
from .homes import HomeSelector


class MenuItem(BaseModel):
    key: str
    title: str
    end: bool


class CoreSelector:
    ...

    @classmethod
    def initial_props(cls, request: HttpRequest) -> CoreInitialPropsRecord:

        if not request.user or not request.user.is_authenticated:
            return None

        user = request.user
        menu = cls.menu_for_user(user=user)
        user_record = UserRecord.from_user(user=user)
        available_homes = HomeSelector.for_user(user_id=user.id)

        return CoreInitialPropsRecord(
            menu=menu,
            config=CoreConfigRecord(is_production=False),
            current_user=user_record,
            available_homes=available_homes,
        )

    @classmethod
    def menu_for_user(
        cls, user: User | None = None, user_id: int | None = None
    ) -> list[MenuItem]:
        user_obj: User

        if user:
            user_obj = user
        elif user_id:
            try:
                user_obj = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise ApplicationError(message="User does not exist.")
        else:
            raise RuntimeError("Either user or user_id must be defined.")

        if user_obj.is_staff:
            return [CoreMenuItemRecord(**item.dict()) for item in MENU]

        # Filter out admin items.
        return [
            CoreMenuItemRecord(**item.dict()) for item in MENU if not item.require_admin
        ]
