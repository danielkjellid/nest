from django.db import models
from django.db.models.fields.mixins import FieldCacheMixin

from nest.core.models import BaseModel

from .enums import RecipeDifficulty, RecipeStatus, RecipeStepType
from .managers import (
    RecipeIngredientItemGroupQuerySet,
    RecipeIngredientItemQuerySet,
    RecipeQuerySet,
    RecipeStepQuerySet,
)

_RecipeManager = models.Manager.from_queryset(RecipeQuerySet)


class Recipe(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50)
    default_num_portions = models.PositiveIntegerField(default=4)
    search_keywords = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Separate with spaces. Title is included by default.",
    )

    external_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Recipe identifier on a provider's site",
    )
    external_url = models.URLField(
        null=True,
        blank=True,
        help_text="Direct link to the recipe on a provider's site",
    )

    status = models.SmallIntegerField(
        choices=RecipeStatus.choices, default=RecipeStatus.DRAFT
    )
    difficulty = models.SmallIntegerField(
        choices=RecipeDifficulty.choices, default=RecipeDifficulty.EASY
    )
    is_vegetarian = models.BooleanField(default=False)
    is_pescatarian = models.BooleanField(default=False)

    objects = _RecipeManager()

    class Meta:
        verbose_name = "recipe"
        verbose_name_plural = "recipes"

    def __str__(self) -> str:
        return f"{self.title} ({self.id})"


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
    step_type = models.PositiveIntegerField(choices=RecipeStepType.choices)

    objects = _RecipeStepManager()

    class Meta:
        verbose_name = "step"
        verbose_name_plural = "steps"

    def __str__(self) -> str:
        return f"Step {self.number}, recipe {self.recipe_id}"

    def get_step_type(self) -> RecipeStepType:
        return RecipeStepType(self.step_type)


_RecipeIngredientItemGroupManager = models.Manager.from_queryset(
    RecipeIngredientItemGroupQuerySet
)


class RecipeIngredientItemGroup(BaseModel, FieldCacheMixin):
    recipe = models.ForeignKey(
        "recipes.Recipe", related_name="ingredient_groups", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    ordering = models.PositiveIntegerField()

    objects = _RecipeIngredientItemGroupManager()

    class Meta:
        verbose_name = "ingredient group"
        verbose_name_plural = "ingredient groups"

    def __str__(self) -> str:
        return f"{self.title} ({self.id}), recipe {self.recipe_id}"


_RecipeIngredientItemManager = models.Manager.from_queryset(
    RecipeIngredientItemQuerySet
)


class RecipeIngredientItem(BaseModel):
    ingredient_group = models.ForeignKey(
        "recipes.RecipeIngredientItemGroup",
        related_name="ingredient_items",
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        "ingredients.Ingredient",
        related_name="ingredient_items",
        on_delete=models.CASCADE,
    )
    step = models.ForeignKey(
        "recipes.RecipeStep",
        related_name="ingredient_items",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    additional_info = models.CharField(max_length=255, null=True, blank=True)

    # The per-portion quantity of the ingredient The portion quantity is multiplied
    # with the number of portions to calculate the quantity of the final product.
    portion_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    portion_quantity_unit = models.ForeignKey(
        "units.Unit", related_name="+", on_delete=models.PROTECT
    )

    objects = _RecipeIngredientItemManager()

    class Meta:
        verbose_name = "ingredient item"
        verbose_name_plural = "ingredient items"
