from datetime import timedelta
from typing import TYPE_CHECKING

from django.db.models import Count, DurationField, Q, Sum
from django.db.models.functions import Coalesce

from nest.core.managers import BaseQuerySet

from ..steps.enums import RecipeStepType

if TYPE_CHECKING:
    from nest.recipes.core import models


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

    def annotate_num_plan_usages(self) -> BaseQuerySet["models.Recipe"]:
        """
        Annotate how many times this recipe has been used in plans.
        """

        return self.annotate(num_plan_usages=Count("plan_items__recipe_plan"))
