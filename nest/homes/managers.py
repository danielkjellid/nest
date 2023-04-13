from __future__ import annotations
from nest.core.managers import BaseQuerySet


class HomeQuerySet(BaseQuerySet["Home"]):
    def active(self) -> HomeQuerySet:
        return self.filter(is_active=True)
