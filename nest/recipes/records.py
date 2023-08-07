from __future__ import annotations
from pydantic import BaseModel
from nest.products.records import ProductRecord
from .models import RecipeIngredient
from decimal import Decimal


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


class RecipeTableRecord(BaseModel):
    key: str
    title: str
    value: Decimal
    unit: str
    percentage_of_daily_value: Decimal


class RecipeHealthScoreRecord(BaseModel):
    rating: Decimal
    positive_impact: list[RecipeTableRecord]
    negative_impact: list[RecipeTableRecord]


class RecipeRecord(BaseModel):
    title: str
    default_num_portions: int
    health_score: RecipeHealthScoreRecord
    nutrition: list[RecipeTableRecord]
