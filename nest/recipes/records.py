from __future__ import annotations
from pydantic import BaseModel
from nest.products.records import ProductRecord
from .models import RecipeIngredient, Recipe, RecipeIngredientItemGroup
from decimal import Decimal
from .enums import RecipeStatus, RecipeDifficulty
from nest.core.utils import ensure_prefetched_relations
from nest.units.records import UnitRecord


class RecipeRecord(BaseModel):
    id: int
    title: str
    slug: str
    default_num_portions: int
    search_keywords: str | None
    external_id: int | None
    external_url: str | None
    status: RecipeStatus
    difficulty: RecipeDifficulty
    is_partial_recipe: bool
    is_vegetarian: bool
    is_pescatarian: bool

    @classmethod
    def from_recipe(cls, recipe: Recipe) -> RecipeRecord:
        return cls(
            id=recipe.id,
            title=recipe.title,
            slug=recipe.slug,
            default_num_portions=recipe.default_num_portions,
            search_keywords=recipe.search_keywords,
            external_id=recipe.external_id,
            external_url=recipe.external_url,
            status=recipe.status,
            difficulty=recipe.difficulty,
            is_partial_recipe=recipe.is_partial_recipe,
            is_vegetarian=recipe.is_vegetarian,
            is_pescatarian=recipe.is_pescatarian,
        )


class RecipeIngredientRecord(BaseModel):
    id: int
    title: str
    product: ProductRecord

    @classmethod
    def from_ingredient(cls, ingredient: RecipeIngredient) -> RecipeIngredientRecord:
        ensure_prefetched_relations(instance=ingredient, prefetch_keys=["product"])

        return cls(
            id=ingredient.id,
            title=ingredient.title,
            product=ProductRecord.from_product(product=ingredient.product),
        )


class RecipeIngredientItemRecord(BaseModel):
    id: int
    ingredient_group_id: int
    ingredient: RecipeIngredientRecord
    additional_info: str
    portion_quantity: Decimal
    portion_quantity_display: str
    portion_quantity_unit: UnitRecord

    @classmethod
    def from_item(cls, ingredient_item):
        ensure_prefetched_relations(
            instance=ingredient_item,
            prefetch_keys=["ingredient", "portion_quantity_unit"],
        )
        return cls(
            id=ingredient_item.id,
            ingredient_group_id=ingredient_item.ingredient_group_id,
            ingredient=RecipeIngredientRecord.from_ingredient(
                ingredient_item.ingredient
            ),
            additional_info=ingredient_item.additional_info,
            portion_quantity=ingredient_item.portion_quantity,
            portion_quantity_display=ingredient_item.portion_quantity.normalize(),
            portion_quantity_unit=UnitRecord.from_unit(
                ingredient_item.portion_quantity_unit
            ),
        )


class RecipeIngredientItemGroupRecord(BaseModel):
    id: int
    recipe_id: int
    title: str
    ordering: int
    ingredient_items: list[RecipeIngredientItemRecord]

    @classmethod
    def from_group(
        cls, ingredient_item_group: RecipeIngredientItemGroup
    ) -> RecipeIngredientItemGroupRecord:
        ensure_prefetched_relations(
            instance=ingredient_item_group, prefetch_keys=["ingredient_items"]
        )

        return cls(
            id=ingredient_item_group.id,
            recipe_id=ingredient_item_group.recipe_id,
            title=ingredient_item_group.title,
            ordering=ingredient_item_group.ordering,
            ingredient_items=[
                RecipeIngredientItemRecord.from_item(ingredient_item=item)
                for item in ingredient_item_group.ingredient_items.all()
            ],
        )


# TODO: -------------


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


class RecipeGlycemicRecord(BaseModel):
    glycemic_index: Decimal
    glycemic_load: Decimal


class RecipeDetailRecord(BaseModel):
    title: str
    default_num_portions: int

    health_score: RecipeHealthScoreRecord
    nutrition: list[RecipeTableRecord]
    glycemic_values: RecipeGlycemicRecord
