from __future__ import annotations
from pydantic import BaseModel
from .models import (
    Recipe,
    RecipeIngredientItemGroup,
    RecipeStep,
    RecipeIngredientItem,
)
from decimal import Decimal
from .enums import RecipeStatus, RecipeDifficulty, RecipeStepType
from nest.units.records import UnitRecord
from nest.core.decorators import ensure_prefetched_relations, ensure_annotated_values
from datetime import timedelta
from isodate import duration_isoformat
from nest.ingredients.records import IngredientRecord


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
    @ensure_prefetched_relations(instance="item", skip_fields=["step"])
    def from_item(cls, item: RecipeIngredientItem) -> RecipeIngredientItemRecord:
        return cls(
            id=item.id,
            group_title=item.ingredient_group.title,
            ingredient=IngredientRecord.from_ingredient(item.ingredient),
            additional_info=item.additional_info,
            portion_quantity=item.portion_quantity,
            portion_quantity_unit=UnitRecord.from_unit(item.portion_quantity_unit),
            portion_quantity_display="{:f}".format(item.portion_quantity.normalize()),
        )


class RecipeMergedIngredientItemDisplayRecord(BaseModel):
    id: int
    ingredient_id: int
    title: str
    quantity_display: str
    unit_display: str
    additional_info: str | None

    @classmethod
    @ensure_prefetched_relations(
        instance="item", skip_fields=["ingredient_group", "step"]
    )
    def from_item(
        cls, item: RecipeIngredientItem, skip_check: bool = False
    ) -> RecipeMergedIngredientItemDisplayRecord:
        return cls(
            id=item.id,
            ingredient_id=item.ingredient_id,
            title=item.ingredient.title,
            quantity_display="{:f}".format(item.portion_quantity.normalize()),
            unit_display=item.portion_quantity_unit.abbreviation,
            additional_info=item.additional_info,
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
    @ensure_prefetched_relations(instance="group", skip_fields=["recipe"])
    def from_group(cls, group: RecipeIngredientItemGroup, skip_check: bool = False):
        return cls(
            id=group.id,
            title=group.title,
            ordering=group.ordering,
            ingredient_items=[
                RecipeIngredientItemRecord.from_item(item)
                for item in group.ingredient_items.all()
            ],
        )


class RecipeIngredientItemGroupDisplayRecord(BaseModel):
    id: int
    title: str
    ingredients: list[RecipeMergedIngredientItemDisplayRecord]

    @classmethod
    @ensure_prefetched_relations(instance="group")
    def from_group(cls, group: RecipeIngredientItemGroup, skip_check: bool = False):
        return cls(
            id=group.id,
            title=group.title,
            ingredients=[
                RecipeMergedIngredientItemDisplayRecord.from_item(item)
                for item in group.ingredient_items.all()
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
    ingredient_items: list[int]

    @classmethod
    @ensure_prefetched_relations(instance="step", skip_fields=["recipe"])
    def from_step(cls, step: RecipeStep, skip_check: bool = False) -> RecipeStepRecord:
        return cls(
            id=step.id,
            number=step.number,
            duration=step.duration,
            instruction=step.instruction,
            step_type=step.step_type,
            ingredient_items=[1],
        )


class RecipeStepDisplayRecord(BaseModel):
    id: int
    number: int
    instruction: str
    ingredients: list[RecipeMergedIngredientItemDisplayRecord]

    @classmethod
    @ensure_prefetched_relations(instance="step", skip_fields=["recipe"])
    def from_step(
        cls, step: RecipeStep, skip_check: bool = False
    ) -> RecipeStepDisplayRecord:
        return cls(
            id=step.id,
            number=step.number,
            instruction=step.instruction,
            ingredients=[
                RecipeMergedIngredientItemDisplayRecord.from_item(item)
                for item in step.ingredient_items.all()
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
    @ensure_annotated_values(
        instance="recipe",
        annotations=["preparation_time", "cooking_time", "total_time"],
    )
    def from_recipe(cls, recipe: Recipe) -> RecipeDurationRecord:
        preparation_time = getattr(recipe, "preparation_time", timedelta(seconds=0))
        cooking_time = getattr(recipe, "cooking_time", timedelta(seconds=0))
        total_time = getattr(recipe, "total_time", timedelta(seconds=0))

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
    difficulty: RecipeDifficulty
    difficulty_display: str
    is_vegetarian: bool
    is_pescatarian: bool

    @classmethod
    def from_recipe(cls, recipe: Recipe):
        return cls(
            id=recipe.id,
            title=recipe.title,
            slug=recipe.slug,
            default_num_portions=recipe.default_num_portions,
            search_keywords=recipe.search_keywords,
            external_id=recipe.external_id,
            external_url=recipe.external_url,
            status=RecipeStatus(recipe.status),
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
    ingredient_groups_display: list[RecipeIngredientItemGroupDisplayRecord]
    steps: list[RecipeStepRecord]
    steps_display: list[RecipeStepDisplayRecord]

    @classmethod
    @ensure_prefetched_relations(instance="recipe")
    def from_recipe(cls, recipe: Recipe, *, skip_check: bool = False):
        steps = recipe.steps.all()
        ingredient_item_groups = recipe.ingredient_groups.all()
        return cls(
            **RecipeRecord.from_recipe(recipe).dict(),
            duration=RecipeDurationRecord.from_recipe(recipe),
            glycemic_data=None,
            health_score=None,
            ingredient_groups=[
                RecipeIngredientItemGroupRecord.from_group(group)
                for group in ingredient_item_groups
            ],
            ingredient_groups_display=[
                RecipeIngredientItemGroupDisplayRecord.from_group(group)
                for group in ingredient_item_groups
            ],
            steps=[RecipeStepRecord.from_step(step) for step in steps],
            steps_display=[RecipeStepDisplayRecord.from_step(step) for step in steps],
        )
