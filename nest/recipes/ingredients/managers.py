from typing import TYPE_CHECKING

from nest.core.managers import BaseQuerySet

if TYPE_CHECKING:
    from nest.recipes.ingredients import models  # noqa


class RecipeIngredientQuerySet(BaseQuerySet["models.RecipeIngredient"]):
    ...


class RecipeIngredientItemQuerySet(BaseQuerySet["models.RecipeIngredientItem"]):
    ...


class RecipeIngredientItemGroupQuerySet(
    BaseQuerySet["models.RecipeIngredientItemGroup"]
):
    ...
