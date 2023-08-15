from typing import TYPE_CHECKING

from nest.core.managers import BaseQuerySet

if TYPE_CHECKING:
    from nest.recipes import models  # noqa


class RecipeQuerySet(BaseQuerySet["models.Recipe"]):
    ...


class RecipeStepQuerySet(BaseQuerySet["models.RecipeStep"]):
    ...


class RecipeIngredientItemGroupQuerySet(
    BaseQuerySet["models.RecipeIngredientItemGroup"]
):
    ...


class RecipeIngredientItemQuerySet(BaseQuerySet["models.RecipeIngredientItem"]):
    ...


class RecipeIngredientQuerySet(BaseQuerySet["models.RecipeIngredient"]):
    ...
