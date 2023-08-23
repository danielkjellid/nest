from __future__ import annotations

from pydantic import BaseModel

from nest.core.decorators import ensure_prefetched_relations
from nest.products.records import ProductRecord

from .models import Ingredient


class IngredientRecord(BaseModel):
    id: int
    title: str
    product: ProductRecord

    @classmethod
    @ensure_prefetched_relations(
        arg_or_kwarg="ingredient", skip_fields=["ingredient_items"]
    )
    def from_ingredient(
        cls, ingredient: Ingredient, skip_check: bool = False
    ) -> IngredientRecord:
        return cls(
            id=ingredient.id,
            title=ingredient.title,
            product=ProductRecord.from_product(ingredient.product),
        )
