from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from isodate import duration_isoformat
from pydantic import BaseModel

from nest.ingredients.records import IngredientRecord
from nest.units.records import UnitRecord

from .enums import RecipeDifficulty, RecipeStatus, RecipeStepType
from .models import (
    Recipe,
    RecipeIngredientItem,
    RecipeIngredientItemGroup,
    RecipeStep,
)

####################
# Ingredient items #
####################


class RecipeIngredientItemRecord(BaseModel):
    id: int
    group_title: str
    ingredient: IngredientRecord
    additional_info: str | None
    portion_quantity: Decimal
    portion_quantity_unit: UnitRecord
    portion_quantity_display: str

    @classmethod
    def from_db_model(cls, model: RecipeIngredientItem) -> RecipeIngredientItemRecord:
        return cls(
            id=model.id,
            group_title=model.ingredient_group.title,
            ingredient=IngredientRecord.from_db_model(model.ingredient),
            additional_info=model.additional_info,
            portion_quantity=model.portion_quantity,
            portion_quantity_display="{:f}".format(model.portion_quantity.normalize()),
            portion_quantity_unit=UnitRecord.from_unit(model.portion_quantity_unit),
        )


##########################
# Ingredient item groups #
##########################


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


#########
# Steps #
#########


class RecipeStepRecord(BaseModel):
    id: int
    number: int
    duration: timedelta
    instruction: str
    step_type: RecipeStepType
    step_type_display: str
    ingredient_items: list[RecipeIngredientItemRecord]

    @classmethod
    def from_db_model(cls, model: RecipeStep) -> RecipeStepRecord:
        return cls(
            id=model.id,
            number=model.number,
            duration=model.duration,
            instruction=model.instruction,
            step_type=RecipeStepType(model.step_type),
            step_type_display=RecipeStepType(model.step_type).label,
            ingredient_items=[
                RecipeIngredientItemRecord.from_db_model(ingredient_item)
                for ingredient_item in model.ingredient_items.all()
            ],
        )


##########
# Recipe #
##########


class RecipeDurationRecord(BaseModel):
    preparation_time: timedelta
    preparation_time_iso8601: str
    cooking_time: timedelta
    cooking_time_iso8601: str
    total_time: timedelta
    total_time_iso8601: str

    @classmethod
    def from_db_model(cls, model: Recipe) -> RecipeDurationRecord:
        preparation_time = getattr(model, "preparation_time", timedelta(seconds=0))
        cooking_time = getattr(model, "cooking_time", timedelta(seconds=0))
        total_time = getattr(model, "total_time", timedelta(seconds=0))

        return cls(
            preparation_time=preparation_time,
            preparation_time_iso8601=duration_isoformat(preparation_time),
            cooking_time=cooking_time,
            cooking_time_iso8601=duration_isoformat(cooking_time),
            total_time=total_time,
            total_time_iso8601=duration_isoformat(total_time),
        )


class RecipeGlycemicData(BaseModel):
    glycemic_index: Decimal
    glycemic_index_rating: str
    glycemic_index_rating_display: str
    glycemic_load: Decimal
    glycemic_load_rating: str
    glycemic_load_rating_display: str


class RecipeHealthScoreImpactRecord(BaseModel):
    key: str
    title: str
    value: Decimal
    value_display: str
    unit_display: str
    percentage_of_daily_value: Decimal
    percentage_of_daily_value_display: str


class RecipeHealthScore(BaseModel):
    rating: Decimal
    positive_impact: list[RecipeHealthScoreImpactRecord]
    negative_impact: list[RecipeHealthScoreImpactRecord]


class RecipeRecord(BaseModel):
    id: int
    title: str
    slug: str
    default_num_portions: int
    search_keywords: str | None
    external_id: str | None
    external_url: str | None
    status: RecipeStatus
    status_display: str
    difficulty: RecipeDifficulty
    difficulty_display: str
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
            status=RecipeStatus(recipe.status),
            status_display=RecipeStatus(recipe.status).label,
            difficulty=RecipeDifficulty(recipe.difficulty),
            difficulty_display=RecipeDifficulty(recipe.difficulty).label,
            is_vegetarian=recipe.is_vegetarian,
            is_pescatarian=recipe.is_pescatarian,
        )


class RecipeDetailRecord(RecipeRecord):
    duration: RecipeDurationRecord
    glycemic_data: RecipeGlycemicData | None  # TODO: Needs to be annotated
    health_score: RecipeHealthScore | None  # TODO: Needs to be annotated
    ingredient_groups: list[RecipeIngredientItemGroupRecord]
    steps: list[RecipeStepRecord]

    @classmethod
    def from_db_model(
        cls,
        *,
        model: Recipe,
        ingredient_groups: list[RecipeIngredientItemGroupRecord],
        steps: list[RecipeStepRecord],
    ) -> RecipeDetailRecord:
        return cls(
            **RecipeRecord.from_recipe(model).dict(),
            duration=RecipeDurationRecord.from_recipe(model),
            glycemic_data=None,
            health_score=None,
            ingredient_groups=ingredient_groups,
            steps=steps,
        )
