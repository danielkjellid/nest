from django.db import models

from nest.core.models import BaseModel

from .enums import RecipeStepType
from .managers import (
    RecipeStepQuerySet,
)

_RecipeStepManager = models.Manager.from_queryset(RecipeStepQuerySet)


class RecipeStep(BaseModel):
    """
    A recipe step can either contain a step item or another recipe in its entirety.
    In that case, all steps of that recipe will be embedded.
    """

    recipe = models.ForeignKey(
        "recipes.Recipe", related_name="steps", on_delete=models.CASCADE
    )
    number = models.PositiveIntegerField()
    duration = models.DurationField()
    instruction = models.TextField()
    step_type = models.CharField(choices=RecipeStepType.choices, max_length=20)

    objects = _RecipeStepManager()

    class Meta:
        verbose_name = "step"
        verbose_name_plural = "steps"

    def __str__(self) -> str:
        return f"Step {self.number}, recipe {self.recipe_id}"

    def get_step_type(self) -> RecipeStepType:
        return RecipeStepType(self.step_type)
