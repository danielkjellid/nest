from django.db import models

from nest.core.models import BaseModel

from .managers import (
    RecipeIngredientItemGroupQuerySet,
    RecipeIngredientItemQuerySet,
    RecipeIngredientQuerySet,
)

_RecipeIngredientManager = models.Manager.from_queryset(RecipeIngredientQuerySet)


class RecipeIngredient(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    product = models.OneToOneField(
        "products.Product",
        related_name="ingredient",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    objects = _RecipeIngredientManager()

    class Meta:
        verbose_name = "ingredient"
        verbose_name_plural = "ingredients"


_RecipeIngredientItemManager = models.Manager.from_queryset(
    RecipeIngredientItemQuerySet
)


class RecipeIngredientItem(BaseModel):
    ingredient_group = models.ForeignKey(
        "recipes_ingredients.RecipeIngredientItemGroup",
        related_name="ingredient_items",
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        "recipes_ingredients.RecipeIngredient",
        related_name="ingredient_items",
        on_delete=models.CASCADE,
    )

    additional_info = models.CharField(max_length=255, null=True, blank=True)

    # The per-portion quantity of the ingredient. The portion quantity is multiplied
    # with the number of portions to calculate the quantity of the final product.
    portion_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    portion_quantity_unit = models.ForeignKey(
        "units.Unit", related_name="+", on_delete=models.PROTECT
    )

    objects = _RecipeIngredientItemManager()

    class Meta:
        verbose_name = "ingredient item"
        verbose_name_plural = "ingredient items"


_RecipeIngredientItemGroupManager = models.Manager.from_queryset(
    RecipeIngredientItemGroupQuerySet
)


class RecipeIngredientItemGroup(BaseModel):
    recipe = models.ForeignKey(
        "recipes.Recipe",
        related_name="ingredient_groups",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    ordering = models.PositiveIntegerField()

    objects = _RecipeIngredientItemGroupManager()

    class Meta:
        verbose_name = "ingredient group"
        verbose_name_plural = "ingredient groups"

    def __str__(self) -> str:
        return f"{self.title} ({self.id}), recipe {self.recipe_id}"
