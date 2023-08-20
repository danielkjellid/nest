from nest.core.managers import BaseQuerySet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nest.ingredients import models  # noqa


class IngredientQuerySet(BaseQuerySet["models.Ingredient"]):
    ...
