from datetime import timedelta
from typing import TYPE_CHECKING

from django.db.models import DurationField, Q, Sum, F, OuterRef, Subquery
from django.db.models.functions import Coalesce

from nest.core.managers import BaseQuerySet
from nest.products.models import Product
from .enums import RecipeStepType

if TYPE_CHECKING:
    from nest.recipes import models


class RecipeQuerySet(BaseQuerySet["models.Recipe"]):
    def annotate_duration(self) -> BaseQuerySet["models.Recipe"]:
        """
        Annotate a recipes duration by calculating the associated steps in the
        respective preparation and cooking step types.
        """
        return self.annotate(
            preparation_time=Coalesce(
                Sum(
                    "steps__duration",
                    filter=(Q(steps__step_type=RecipeStepType.PREPARATION)),
                    output_field=DurationField(),
                ),
                timedelta(seconds=0),
            ),
            cooking_time=Coalesce(
                Sum(
                    "steps__duration",
                    filter=(Q(steps__step_type=RecipeStepType.COOKING)),
                    output_field=DurationField(),
                ),
                timedelta(seconds=0),
            ),
            total_time=Coalesce(
                Sum("steps__duration", output_field=DurationField()),
                timedelta(seconds=0),
            ),
        )


class RecipeStepQuerySet(BaseQuerySet["models.RecipeStep"]):
    ...


class RecipeIngredientItemGroupQuerySet(
    BaseQuerySet["models.RecipeIngredientItemGroup"]
):
    ...


class RecipeIngredientItemQuerySet(BaseQuerySet["models.RecipeIngredientItem"]):
    ...
