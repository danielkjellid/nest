from datetime import timedelta

from pydantic import BaseModel

from ..ingredients.records import RecipeIngredientItemRecord
from .enums import RecipeStepType


class RecipeStepRecord(BaseModel):
    id: int
    number: int
    duration: timedelta
    instruction: str
    step_type: RecipeStepType
    step_type_display: str
    ingredient_items: list[RecipeIngredientItemRecord]
