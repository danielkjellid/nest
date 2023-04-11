from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel

from nest.models import Product

from .units import UnitRecord


class ProductRecord(BaseModel):
    id: int
    name: str
    gross_price: Decimal
    gross_unit_price: Decimal | None
    unit: UnitRecord
    unit_quantity: Decimal | None
    oda_url: str | None
    oda_id: int | None
    is_available: bool
    thumbnail_url: str | None
    gtin: str | None
    supplier: str

    @classmethod
    def from_product(cls, product: Product) -> ProductRecord:
        return cls(
            id=product.id,
            name=product.name,
            gross_price=product.gross_price,
            gross_unit_price=product.gross_unit_price,
            unit=UnitRecord.from_unit(product.unit),
            unit_quantity=product.unit_quantity,
            oda_id=product.oda_id,
            oda_url=product.oda_url,
            is_available=product.is_available,
            thumbnail_url=product.thumbnail.url if product.thumbnail else None,
            gtin=product.gtin,
            supplier=product.supplier,
        )
