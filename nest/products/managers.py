from __future__ import annotations

from nest.core.managers import BaseQuerySet


class ProductQuerySet(BaseQuerySet["Product"]):
    ...
