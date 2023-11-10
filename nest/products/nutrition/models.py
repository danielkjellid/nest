from nest.core.models import BaseModel
from django.db import models
from .managers import ProductNutritionQuerySet
from typing import ClassVar

_ProductNutritionManager = models.Manager.from_queryset(ProductNutritionQuerySet)


class ProductNutrition(BaseModel):
    """
    Product nutrition holds nutritional information for a product and is noted in per
    100gr/ml.
    """

    products = models.OneToOneField(
        "products.Product", related_name="nutrition", on_delete=models.CASCADE
    )
    # Nutritional information (per 100 gr/ml)
    energy_kj = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    energy_kcal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    fat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    fat_saturated = models.DecimalField(  # "hvorav mettede fettsyrer"
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    fat_monounsaturated = models.DecimalField(  # "hvorav enumettede fettsyrer"
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    fat_polyunsaturated = models.DecimalField(  # "hvorav flerumettede fettsyrer"
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    carbohydrates = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    carbohydrates_sugars = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    carbohydrates_polyols = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    carbohydrates_starch = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    fibres = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    protein = models.DecimalField(
        "protein",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    salt = models.DecimalField(
        "salt",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    sodium = models.DecimalField(
        "sodium",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    objects = _ProductNutritionManager()

    class Meta:
        verbose_name = "product nutrition"
        verbose_name_plural = "product nutrition"
