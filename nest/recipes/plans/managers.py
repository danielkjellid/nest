from typing import TYPE_CHECKING

from nest.core.managers import BaseQuerySet

if TYPE_CHECKING:
    from nest.recipes.plans import models  # noqa


class RecipePlanQuerySet(BaseQuerySet["models.RecipePlan"]):
    ...


class RecipePlanItemQuerySet(BaseQuerySet["models.RecipePlanItem"]):
    ...
