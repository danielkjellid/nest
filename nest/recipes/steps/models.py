from django.db import models

from nest.core.models import BaseModel

from .enums import RecipeStepType
from .managers import (
    RecipeStepIngredientItemQuerySet,
    RecipeStepQuerySet,
)

_RecipeStepManager = models.Manager.from_queryset(RecipeStepQuerySet)


class RecipeStep(BaseModel):
    """
    A recipe step which gives instructions on a certain part of a recipe.
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

    @property
    def get_step_type(self) -> RecipeStepType:
        return RecipeStepType(self.step_type)

    @property
    def duration_minutes(self) -> int:
        return round(self.duration.seconds / 60)


_RecipeStepIngredientItemManager = models.Manager.from_queryset(
    RecipeStepIngredientItemQuerySet
)


class RecipeStepIngredientItem(BaseModel):
    """
    A RecipeStepIngredientItem connects a step and an ingredient item.
    """

    step = models.ForeignKey(
        RecipeStep,
        related_name="ingredient_items",
        on_delete=models.CASCADE,
    )
    ingredient_item = models.ForeignKey(
        "recipes_ingredients.RecipeIngredientItem",
        related_name="steps",
        on_delete=models.CASCADE,
    )

    objects = _RecipeStepIngredientItemManager()
