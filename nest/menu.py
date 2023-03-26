from typing import Final
from nest.records import CoreMenuItemRecord
from pydantic import BaseModel


class MenuItem(BaseModel):
    key: str
    title: str
    end: bool
    require_admin: bool


MENU: Final[list[CoreMenuItemRecord]] = [
    MenuItem(key="plans", title="Meal plans", end=True, require_admin=False),
    MenuItem(key="products", title="Products", end=True, require_admin=False),
    MenuItem(key="recipes", title="Recipes", end=True, require_admin=False),
    MenuItem(key="settings", title="Settings", end=True, require_admin=False),
    MenuItem(key="users", title="Users", end=True, require_admin=True),
]
