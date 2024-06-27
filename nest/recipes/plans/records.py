from datetime import datetime

from pydantic import BaseModel

from nest.recipes.core.records import RecipeRecord


class RecipePlanItemRecord(BaseModel):
    id: int
    plan_id: int
    plan_title: str
    recipe: RecipeRecord


class RecipePlanRecord(BaseModel):
    id: int
    title: str
    description: str
    slug: str
    from_date: datetime
    items: list[RecipePlanItemRecord]
