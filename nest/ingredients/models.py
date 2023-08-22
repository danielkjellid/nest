from django.db import models

from nest.core.models import BaseModel

from .managers import IngredientQuerySet

_IngredientManager = models.Manager.from_queryset(IngredientQuerySet)


class Ingredient(BaseModel):
    # A friendly (alternative) title for ingredient, used in cases where the title is
    # 'Tomatoes, red' and the friendly/display name would be 'Red tomatoes'.
    title = models.CharField(max_length=255, unique=True)
    product = models.OneToOneField(
        "products.Product",
        related_name="ingredient",
        on_delete=models.CASCADE,
    )

    objects = _IngredientManager()

    class Meta:
        verbose_name = "ingredient"
        verbose_name_plural = "ingredients"
