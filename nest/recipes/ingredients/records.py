from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel

from nest.products.core.records import ProductRecord
from nest.units.records import UnitRecord

from .models import RecipeIngredient, RecipeIngredientItem, RecipeIngredientItemGroup


class RecipeIngredientRecord(BaseModel):
    id: int
    title: str
    product: ProductRecord | None
    is_base_ingredient: bool = False

    @classmethod
    def from_db_model(cls, model: RecipeIngredient) -> RecipeIngredientRecord:
        return cls(
            id=model.id,
            title=model.title,
            product=ProductRecord.from_product(model.product)
            if model.product
            else None,
            is_base_ingredient=model.is_base_ingredient,
        )


class RecipeIngredientItemRecord(BaseModel):
    id: int
    group_title: str
    ingredient: RecipeIngredientRecord
    additional_info: str | None
    portion_quantity: Decimal
    portion_quantity_unit: UnitRecord
    portion_quantity_display: str

    @classmethod
    def from_db_model(cls, model: RecipeIngredientItem) -> RecipeIngredientItemRecord:
        return cls(
            id=model.id,
            group_title=model.ingredient_group.title,
            ingredient=RecipeIngredientRecord.from_db_model(model.ingredient),
            additional_info=model.additional_info,
            portion_quantity=model.portion_quantity,
            portion_quantity_display="{:f}".format(model.portion_quantity.normalize()),
            portion_quantity_unit=UnitRecord.from_unit(model.portion_quantity_unit),
        )


class RecipeIngredientItemGroupRecord(BaseModel):
    id: int
    title: str
    ordering: int
    ingredient_items: list[RecipeIngredientItemRecord]

    @classmethod
    def from_db_model(
        cls,
        model: RecipeIngredientItemGroup,
    ) -> RecipeIngredientItemGroupRecord:
        return cls(
            id=model.id,
            title=model.title,
            ordering=model.ordering,
            ingredient_items=[
                RecipeIngredientItemRecord.from_db_model(item)
                for item in model.ingredient_items.all()
            ],
        )
