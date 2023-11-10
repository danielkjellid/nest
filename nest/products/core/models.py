from __future__ import annotations

import os
from decimal import Decimal
from typing import ClassVar

from django.db import models

from nest.core.models import BaseModel
from nest.core.utils import format_datetime

from .managers import ProductQuerySet

_ProductManager = models.Manager.from_queryset(ProductQuerySet)


class Product(BaseModel):
    def get_product_upload_path(self, filename: str) -> str:
        name, extension = os.path.splitext(filename)
        return f"products/thumbnails/{name}{extension}"

    name = models.CharField(max_length=255)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2)
    gross_unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    unit = models.ForeignKey(
        "units.Unit",
        related_name="products",
        on_delete=models.PROTECT,
    )
    unit_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    is_available = models.BooleanField(default=True)
    thumbnail = models.ImageField(
        upload_to=get_product_upload_path,
        blank=True,
        null=True,
    )
    gtin = models.CharField(max_length=14, null=True, blank=True)
    supplier = models.CharField(max_length=50, null=True, blank=True)
    ingredients = models.TextField(null=True, blank=True)
    allergens = models.TextField(null=True, blank=True)

    # Classifiers/allergens
    contains_gluten = models.BooleanField(default=False)
    contains_lactose = models.BooleanField(default=False)

    # Data pools
    oda_id = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    oda_url = models.CharField(max_length=255, blank=True, null=True)
    is_synced = models.BooleanField(
        default=True, help_text="Product is kept in sync from Oda."
    )
    last_data_update = models.DateTimeField(
        blank=True,
        null=True,
        help_text="The last time the data was automatically updated.",
    )

    objects = _ProductManager()

    ADMIN_LIST_DISPLAY: ClassVar = [
        "name",
        "gross_price",
        "unit",
        "oda_id",
        "oda_url",
        "is_available",
    ]

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    @property
    def full_name(self) -> str:
        if self.unit_quantity is not None:
            return (
                f"{self.name}, "
                f"{Decimal(self.unit_quantity).normalize()} {self.unit.abbreviation}"
            )
        return self.name

    @property
    def display_price(self) -> str:
        if self.unit is not None and self.gross_unit_price is not None:
            return f"{self.gross_price} kr ({self.gross_unit_price} per {self.unit.abbreviation})"
        return f"{self.gross_price}"

    @property
    def is_oda_product(self) -> bool:
        return self.oda_id is not None

    @property
    def last_synced_at(self) -> str | None:
        return (
            format_datetime(self.updated_at, with_seconds=True)
            if self.updated_at
            else None
        )
