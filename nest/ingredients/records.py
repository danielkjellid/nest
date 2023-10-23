from __future__ import annotations

from pydantic import BaseModel

from nest.core.utils import get_related_field
from nest.products.records import ProductRecord
from nest.core.decorators import ensure_no_fetch

from .models import Ingredient


class IngredientRecord(BaseModel):
    id: int
    title: str
    product: ProductRecord

    @classmethod
    @ensure_no_fetch
    def from_db_model(cls, model: Ingredient) -> IngredientRecord:
        product = get_related_field(model, "product")

        return cls(
            id=model.id,
            title=model.title,
            product=ProductRecord.from_product(product),
        )
