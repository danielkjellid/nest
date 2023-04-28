from __future__ import annotations

import os
from decimal import Decimal

from django.db import models

from nest.core.models import BaseModel
from nest.core.utils.dates import DateUtil

from .managers import ProductQuerySet

_ProductManager = models.Manager.from_queryset(ProductQuerySet)


class Product(BaseModel):
    def get_product_upload_path(self, filename: str) -> str:
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
    oda_url = models.CharField(max_length=255, blank=True, null=True)
    oda_id = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    is_available = models.BooleanField(default=True)
    thumbnail = models.ImageField(
        upload_to=get_product_upload_path,
        blank=True,
        null=True,
    )
    gtin = models.CharField(max_length=14, null=True, blank=True)
    supplier = models.CharField(max_length=50)
    is_synced = models.BooleanField(
        default=True, help_text="Product is kept in sync from Oda."
    )

    ADMIN_LIST_DISPLAY = [
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
            DateUtil.format_datetime(self.updated_at, with_seconds=True)
            if self.updated_at
            else None
        )
