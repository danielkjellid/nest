from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from isodate import duration_isoformat
from pydantic import BaseModel

from .enums import RecipeDifficulty, RecipeStatus
from .models import Recipe
from ..steps.records import RecipeStepRecord
from ..ingredients.records import RecipeIngredientItemGroupRecord


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

    @classmethod
    def from_datetime(
        cls, preparation_time: timedelta, cooking_time: timedelta, total_time: timedelta
    ):
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
