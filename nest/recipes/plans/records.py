from datetime import datetime

from pydantic import BaseModel

from nest.recipes.core.records import RecipeDetailRecord


class RecipePlanItemRecord(BaseModel):
    id: int
    plan_id: int
    plan_title: str
    recipe: RecipeDetailRecord


class RecipePlanRecord(BaseModel):
    id: int
    title: str
    description: str | None
    slug: str
    from_date: datetime | None
    items: list[RecipePlanItemRecord]
