from pydantic import BaseModel
from datetime import timedelta
from .enums import RecipeStepType
from ..ingredients.records import RecipeIngredientItemRecord


class RecipeStepRecord(BaseModel):
    id: int
    number: int
    duration: timedelta
    instruction: str
    step_type: RecipeStepType
    step_type_display: str
    ingredient_items: list[RecipeIngredientItemRecord]
