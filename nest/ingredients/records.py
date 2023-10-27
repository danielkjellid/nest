from __future__ import annotations

from pydantic import BaseModel

from nest.products.records import ProductRecord

from .models import Ingredient


class IngredientRecord(BaseModel):
    id: int
    title: str
    product: ProductRecord

    @classmethod
    def from_db_model(cls, model: Ingredient) -> IngredientRecord:
        return cls(
            id=model.id,
            title=model.title,
            product=ProductRecord.from_product(model.product),
        )
