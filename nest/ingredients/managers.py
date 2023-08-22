from typing import TYPE_CHECKING

from nest.core.managers import BaseQuerySet

if TYPE_CHECKING:
    from nest.ingredients import models  # noqa


class IngredientQuerySet(BaseQuerySet["models.Ingredient"]):
    ...
