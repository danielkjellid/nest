from __future__ import annotations
from pydantic import BaseModel
from nest.products.records import ProductRecord
from .models import (
    RecipeIngredient,
    Recipe,
    RecipeIngredientItemGroup,
    RecipeStep,
    RecipeIngredientItem,
)
from isodate import duration_isoformat
from decimal import Decimal
from .enums import RecipeStatus, RecipeDifficulty, RecipeStepType
from nest.units.records import UnitRecord
from nest.core.decorators import ensure_prefetched_relations, ensure_annotated_values
from datetime import timedelta


# class RecipeIngredientRecord(BaseModel):
#     id: int
#     title: str
#     product: ProductRecord
#
#     @classmethod
#     def from_ingredient(cls, ingredient: RecipeIngredient) -> RecipeIngredientRecord:
#         ensure_prefetched_relations(instance=ingredient, prefetch_keys=["product"])
#
#         return cls(
#             id=ingredient.id,
#             title=ingredient.title,
#             product=ProductRecord.from_product(product=ingredient.product),
#         )
#
#
# class RecipeIngredientItemRecord(BaseModel):
#     id: int
#     ingredient_group_id: int
#     ingredient: RecipeIngredientRecord
#     additional_info: str
#     portion_quantity: Decimal
#     portion_quantity_display: str
#     portion_quantity_unit: UnitRecord
#
#     @classmethod
#     def from_item(cls, ingredient_item):
#         ensure_prefetched_relations(
#             instance=ingredient_item,
#             prefetch_keys=["ingredient", "portion_quantity_unit"],
#         )
#         return cls(
#             id=ingredient_item.id,
#             ingredient_group_id=ingredient_item.ingredient_group_id,
#             ingredient=RecipeIngredientRecord.from_ingredient(
#                 ingredient_item.ingredient
#             ),
#             additional_info=ingredient_item.additional_info,
#             portion_quantity=ingredient_item.portion_quantity,
#             portion_quantity_display=ingredient_item.portion_quantity.normalize(),
#             portion_quantity_unit=UnitRecord.from_unit(
#                 ingredient_item.portion_quantity_unit
#             ),
#         )
#
#
# # class RecipeIngredientItemDetailRecord(BaseModel):
# #     id: int
# #     ingredient_group: RecipeIngredientItemGroup
# #     ingredient: RecipeIngredientRecord
# #     additional_info: str
# #     portion_quantity: Decimal
# #     portion_quantity_display: str
# #     portion_quantity_unit: UnitRecord
# #
# #     @classmethod
# #     def from_item(cls, item: RecipeIngredientItem) -> RecipeIngredientItemDetailRecord:
# #         return cls(
# #            id=item.id,
# #            ingredient_group=
# #         )
#
#
# class RecipeIngredientItemGroupRecord(BaseModel):
#     id: int
#     recipe_id: int
#     title: str
#     ordering: int
#     ingredient_items: list[RecipeIngredientItemRecord]
#
#     @classmethod
#     def from_group(
#         cls, ingredient_item_group: RecipeIngredientItemGroup
#     ) -> RecipeIngredientItemGroupRecord:
#         ensure_prefetched_relations(
#             instance=ingredient_item_group, prefetch_keys=["ingredient_items"]
#         )
#
#         return cls(
#             id=ingredient_item_group.id,
#             recipe_id=ingredient_item_group.recipe_id,
#             title=ingredient_item_group.title,
#             ordering=ingredient_item_group.ordering,
#             ingredient_items=[
#                 RecipeIngredientItemRecord.from_item(ingredient_item=item)
#                 for item in ingredient_item_group.ingredient_items.all()
#             ],
#         )
#
#
# class RecipeStepRecord(BaseModel):
#     id: int
#     recipe_id: int
#     number: int
#     duration: timedelta
#     instruction: str
#     step_type: RecipeStepType
#     ingredient_items: list[RecipeIngredientItemRecord]
#
#     @classmethod
#     def from_step(cls, step: RecipeStep) -> RecipeStepRecord:
#         ensure_prefetched_relations(instance=step, prefetch_keys=["ingredient_items"])
#         return cls(
#             id=step.id,
#             recipe_id=step.recipe_id,
#             number=step.number,
#             duration=step.duration,
#             instruction=step.instruction,
#             step_type=step.step_type,
#             ingredient_items=[
#                 RecipeIngredientItemRecord.from_item(item)
#                 for item in step.ingredient_items.all()
#             ],
#         )
#
#
# class RecipeRecord(BaseModel):
#     id: int
#     title: str
#     slug: str
#     default_num_portions: int
#     search_keywords: str | None
#     external_id: int | None
#     external_url: str | None
#     status: RecipeStatus
#     difficulty: RecipeDifficulty
#     is_partial_recipe: bool
#     is_vegetarian: bool
#     is_pescatarian: bool
#
#     @classmethod
#     def from_recipe(cls, recipe: Recipe) -> RecipeRecord:
#         return cls(
#             id=recipe.id,
#             title=recipe.title,
#             slug=recipe.slug,
#             default_num_portions=recipe.default_num_portions,
#             search_keywords=recipe.search_keywords,
#             external_id=recipe.external_id,
#             external_url=recipe.external_url,
#             status=recipe.status,
#             difficulty=recipe.difficulty,
#             is_partial_recipe=recipe.is_partial_recipe,
#             is_vegetarian=recipe.is_vegetarian,
#             is_pescatarian=recipe.is_pescatarian,
#         )
#
#
# class RecipeDetailRecord(RecipeRecord):
#     steps: list[RecipeStepRecord]
#     ingredient_item_groups: list[RecipeIngredientItemGroupRecord]
#
#     @classmethod
#     def from_recipe(cls, recipe: Recipe) -> RecipeDetailRecord:
#         ensure_prefetched_relations(
#             instance=recipe, prefetch_keys=["steps", "ingredient_groups"]
#         )
#
#         return cls(
#             **RecipeRecord.from_recipe(recipe).dict(),
#             steps=[RecipeStepRecord.from_step(step) for step in recipe.steps.all()],
#             ingredient_item_groups=[
#                 RecipeIngredientItemGroupRecord.from_group(group)
#                 for group in recipe.ingredient_groups.all()
#             ],
#         )


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


class RecipeIngredientItemGroupRecord(BaseModel):
    id: int
    title: str
    ordering: int
    ingredient_items: list[RecipeIngredientItemRecord]

    @classmethod
    @ensure_prefetched_relations(instance="group")
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


class RecipeIngredientItemRecord(BaseModel):
    id: int
    group_title: str
    ingredient: RecipeIngredientRecord
    additional_info: str | None
    portion_quantity: Decimal
    portion_quantity_unit: UnitRecord

    @classmethod
    @ensure_prefetched_relations(instance="item", skip_fields=["step"])
    def from_item(cls, item: RecipeIngredientItem) -> RecipeIngredientItemRecord:
        return cls(
            id=item.id,
            group_title=item.ingredient_group.title,
            ingredient=RecipeIngredientRecord.from_ingredient(item.ingredient),
            additional_info=item.additional_info,
            portion_quantity=item.portion_quantity,
            portion_quantity_unit=UnitRecord.from_unit(item.portion_quantity_unit),
        )


class RecipeIngredientRecord(BaseModel):
    id: int
    title: str
    product: ProductRecord

    @classmethod
    @ensure_prefetched_relations(instance="ingredient")
    def from_ingredient(
        cls, ingredient: RecipeIngredient, skip_check: bool = False
    ) -> RecipeIngredientRecord:
        return cls(
            id=ingredient.id,
            title=ingredient.title,
            product=ProductRecord.from_product(ingredient.product),
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
        return cls(
            preparation_time=recipe.preparation_time,  # type: ignore
            preparation_time_iso8601=(
                duration_isoformat(recipe.preparation_time)  # type: ignore
            ),
            cooking_time=recipe.cooking_time,  # type: ignore
            cooking_time_iso8601=(
                duration_isoformat(recipe.cooking_time)  # type: ignore
            ),
            total_time=recipe.total_time,  # type: ignore
            total_time_iso8601=duration_isoformat(recipe.total_time),  # type: ignore
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
    duration: RecipeDurationRecord
    glycemic_data: RecipeGlycemicData | None
    health_score: RecipeHealthScore | None
    ingredient_groups: list[RecipeIngredientItemGroupRecord]
    ingredient_groups_display: list[RecipeIngredientItemGroupDisplayRecord]
    steps: list[RecipeStepRecord]
    steps_display: list[RecipeStepDisplayRecord]


# TODO: -------------


# class RecipeTableRecord(BaseModel):
#     key: str
#     title: str
#     value: Decimal
#     unit: str
#     percentage_of_daily_value: Decimal
#
#
# class RecipeHealthScoreRecord(BaseModel):
#     rating: Decimal
#     positive_impact: list[RecipeTableRecord]
#     negative_impact: list[RecipeTableRecord]
#
#
# class RecipeGlycemicRecord(BaseModel):
#     glycemic_index: Decimal
#     glycemic_load: Decimal


# class RecipeDetailRecord(BaseModel):
#     title: str
#     default_num_portions: int
#
#     health_score: RecipeHealthScoreRecord
#     nutrition: list[RecipeTableRecord]
#     glycemic_values: RecipeGlycemicRecord


desired_payload = {
    "id": 1,
    "title": "Cool Recipe",
    "slug": "cool-recipe",
    "default_num_portions": 4,
    "search_keywords": None,
    "external_id": None,
    "external_url": None,
    "status": RecipeStatus.PUBLISHED,
    "difficulty": RecipeDifficulty.EASY,
    "difficulty_display": "Easy",
    "is_vegetarian": False,
    "is_pescatarian": False,
    "duration": {
        "preparation_time": timedelta(minutes=2),
        "preparation_time_iso8601": "P0DT00H20M00S",
        "preparation_time_display": "2 min",
        "cooking_time": timedelta(minutes=5),
        "cooking_time_iso8601": "P0DT00H20M00S",
        "cooking_time_display": "5 min",
        "total_time": timedelta(minutes=7),
        "total_time_display": "7 min",
        "total_time_iso8601": "P0DT00H20M00S",
    },
    "glycemic_data": {
        "glycemic_index": Decimal("31.2"),
        "glycemic_index_rating": "low",
        "glycemic_index_rating_display": "Low",
        "glycemic_load": Decimal("3.0"),
        "glycemic_load_rating": "low",
        "glycemic_load_rating_display": "Low",
    },
    "health_score": {
        "rating": Decimal("8.9"),
        "positive_impact": [
            {
                "key": "unsaturated_fat",
                "title": "Unsaturated Fat",
                "value": Decimal("14.0"),
                "value_display": "14",
                "unit_display": "g",
                "percentage_of_daily_value": Decimal("29.0"),
            },
            # ...
        ],
        "negative_impact": [
            {
                "key": "unsaturated_fat",
                "title": "Unsaturated Fat",
                "value": Decimal("14.0"),
                "value_display": "14",
                "unit_display": "g",
                "percentage_of_daily_value": Decimal("29.0"),
            },
        ],
    },
    "ingredient_item_groups": [
        {
            "id": 1,
            "title": "Group 1",
            "ordering": 1,
            "ingredient_items": [
                {
                    "id": 1,
                    "group_title": "Group 1",
                    "ingredient": {
                        "id": 1,
                        "title": "Basilikum fersk",
                        "product": {
                            "id": 1,
                            # ...
                        },
                    },
                    "additional_info": None,
                    "portion_quantity": "0.250",
                    "portion_unit": {
                        "id": 1,
                        "type": 2,
                        "type_name": "Vekt",
                        "abbreviation": "g",
                        "name": "gram",
                        "base_factor": 1.0,
                    },
                },
                # ...
            ],
        }
    ],
    "ingredient_item_groups_display": [
        {
            "id": 1,
            "title": "Group 1",
            "ingredients": [
                {
                    "id": 1,
                    "title": "Basilikum fersk",
                    "quantity_display": "210",
                    "unit_display": "g",
                    "additional_info": None,
                }
                # ...
            ],
        }
    ],
    "steps": [
        {
            "id": 1,
            "number": 1,
            "duration": timedelta(minutes=2),
            "instruction": "Some instruction",
            "step_type": RecipeStepType.COOKING,
            "ingredient_items": [
                {
                    "id": 1,
                    "group_title": "Group 1",
                    "ingredient": {
                        "id": 1,
                        "title": "Basilikum fersk",
                        "product": {
                            "id": 1,
                            # ...
                        },
                    },
                    "additional_info": None,
                    "portion_quantity": "0.250",
                    "portion_unit": {
                        "id": 1,
                        "type": 2,
                        "type_name": "Vekt",
                        "abbreviation": "g",
                        "name": "gram",
                        "base_factor": 1.0,
                    },
                },
                # ...
            ],
        }
    ],
    "steps_display": [
        {
            "id": 1,
            "number": 1,
            "instruction": "Some instruction",
            "ingredients": [
                {
                    "id": 1,
                    "title": "Basilikum fersk",
                    "quantity_display": "210",
                    "unit_display": "g",
                    "additional_info": None,
                }
                # ...
            ],
        }
    ],
}
