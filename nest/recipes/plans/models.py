from django.db import models

from nest.core.models import BaseModel

from ..core.models import Recipe
from .managers import RecipePlanItemQuerySet, RecipePlanQuerySet

_RecipePlanManager = models.Manager.from_queryset(RecipePlanQuerySet)


class RecipePlan(BaseModel):
    """
    A recipe plan organizes some recipes under a common title and description.
    Used to crate weekly (or ad-hoc) meal plans.
    """

    title = models.CharField(max_length=50)
    description = models.TextField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=50)
    from_date = models.DateTimeField(blank=True, null=True)
    home = models.ForeignKey(
        "homes.Home",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    objects = _RecipePlanManager()

    def __str__(self) -> str:
        if self.from_date:
            return f"{self.title} - {self.from_date.date()}"
        return self.title


_RecipePlanItemManager = models.Manager.from_queryset(RecipePlanItemQuerySet)


class RecipePlanItem(BaseModel):
    """
    A RecipePlanItem connects a recipe plan and a recipe.
    """

    recipe_plan = models.ForeignKey(
        RecipePlan,
        on_delete=models.CASCADE,
        related_name="plan_items",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="plan_items",
    )
    ordering = models.PositiveIntegerField("ordering")

    objects = _RecipePlanItemManager()

    class Meta:
        ordering = ("ordering",)
