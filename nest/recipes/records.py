from __future__ import annotations
from pydantic import BaseModel
from nest.products.records import ProductRecord
from .models import RecipeIngredient


class RecipeIngredientRecord(BaseModel):
    id: int
    title: str
    product: ProductRecord

    @classmethod
    def from_ingredient(cls, ingredient: RecipeIngredient) -> RecipeIngredientRecord:
        return cls(
            id=ingredient.id,
            title=ingredient.title,
            product=ProductRecord.from_product(product=ingredient.product),
        )
