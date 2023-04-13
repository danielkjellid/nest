from __future__ import annotations

from typing import TYPE_CHECKING

from nest.core.managers import BaseQuerySet

if TYPE_CHECKING:
    from .models import Home  # noqa


class HomeQuerySet(BaseQuerySet["Home"]):
    def active(self) -> HomeQuerySet:
        return self.filter(is_active=True)
