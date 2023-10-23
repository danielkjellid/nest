from typing import TYPE_CHECKING

from nest.core.managers import BaseQuerySet

if TYPE_CHECKING:
    from nest.recipes.steps.models import models  # noqa


class RecipeStepQuerySet(BaseQuerySet["models.RecipeStep"]):
    ...
