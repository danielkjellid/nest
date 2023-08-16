from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from nest.units.records import UnitRecord

from .models import Product
from nest.core.utils import ensure_prefetched_relations


class ProductClassifiersRecord(BaseModel):
    contains_gluten: bool
    contains_lactose: bool

    @classmethod
    def from_product(cls, product: Product) -> ProductClassifiersRecord:
        return cls(
            contains_lactose=product.contains_lactose,
            contains_gluten=product.contains_gluten,
        )


class ProductRecord(BaseModel):
    id: int
    name: str
    full_name: str
    gross_price: Decimal
    gross_unit_price: Decimal | None
    unit: UnitRecord
    unit_quantity: Decimal | None
    oda_url: str | None
    oda_id: int | None
    is_available: bool
    is_synced: bool
    last_synced_at: str | None
    thumbnail_url: str | None
    gtin: str | None
    supplier: str | None
    display_price: str
    is_oda_product: bool
    last_data_update: datetime | None

    ingredients: str | None
    allergens: str | None
    classifiers: ProductClassifiersRecord

    energy_kj: Decimal | None
    energy_kcal: Decimal | None
    fat: Decimal | None
    fat_saturated: Decimal | None
    fat_monounsaturated: Decimal | None
    fat_polyunsaturated: Decimal | None
    carbohydrates: Decimal | None
    carbohydrates_sugars: Decimal | None
    carbohydrates_polyols: Decimal | None
    carbohydrates_starch: Decimal | None
    fibres: Decimal | None
    protein: Decimal | None
    salt: Decimal | None
    sodium: Decimal | None

    @classmethod
    def from_product(cls, product: Product) -> ProductRecord:
        # ensure_prefetched_relations(instance=product, prefetch_keys=["unit"])

        return cls(
            id=product.id,
            name=product.name,
            full_name=product.full_name,
            gross_price=product.gross_price,
            gross_unit_price=product.gross_unit_price,
            unit=UnitRecord.from_unit(product.unit),
            unit_quantity=product.unit_quantity,
            oda_id=product.oda_id,
            oda_url=product.oda_url,
            is_available=product.is_available,
            is_synced=product.is_synced,
            last_synced_at=product.last_synced_at,
            thumbnail_url=product.thumbnail.url if product.thumbnail else None,
            gtin=product.gtin,
            supplier=product.supplier,
            is_oda_product=product.is_oda_product,
            last_data_update=product.last_data_update,
            display_price=product.display_price,
            ingredients=product.ingredients,
            allergens=product.allergens,
            classifiers=ProductClassifiersRecord.from_product(product),
            energy_kj=product.energy_kj,
            energy_kcal=product.energy_kcal,
            fat=product.fat,
            fat_saturated=product.fat_saturated,
            fat_monounsaturated=product.fat_monounsaturated,
            fat_polyunsaturated=product.fat_polyunsaturated,
            carbohydrates=product.carbohydrates,
            carbohydrates_sugars=product.carbohydrates_sugars,
            carbohydrates_polyols=product.carbohydrates_polyols,
            carbohydrates_starch=product.carbohydrates_starch,
            fibres=product.fibres,
            protein=product.protein,
            salt=product.salt,
            sodium=product.sodium,
        )
