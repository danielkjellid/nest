from __future__ import annotations
import os
from django.db import models

from .base import BaseModel, BaseQuerySet


class ProductQuerySet(BaseQuerySet["Product"]):
    ...


_ProductManager = models.Manager.from_queryset(ProductQuerySet)


class Product(BaseModel):
    def get_product_upload_path(self, filename):
        name, extension = os.path.splitext(filename)
        return f"products/{self.id}/{name}{extension}"

    name = models.CharField(max_length=255)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2)
    gross_unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    unit = models.ForeignKey(
        "nest.Unit",
        related_name="products",
        on_delete=models.PROTECT,
    )
    unit_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    oda_url = models.CharField(max_length=255, blank=True, null=True)
    oda_id = models.PositiveBigIntegerField()
    is_available = models.BooleanField(default=True)
    thumbnail = models.ImageField(
        upload_to=get_product_upload_path,
        blank=True,
        null=True,
    )
    gtin = models.CharField(max_length=14)
    supplier = models.CharField(max_length=50)

    ADMIN_LIST_DISPLAY = ["name", "gross_price", "unit", "oda_id", "oda_url"]

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
