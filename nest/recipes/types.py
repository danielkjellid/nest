from typing import TypedDict


class RecipeIngredientItemDict(TypedDict):
    ingredient_id: str
    additional_info: str | None
    portion_quantity: str
    portion_quantity_unit_id: str


class RecipeIngredientItemGroupDict(TypedDict):
    title: str
    ordering: int
    ingredients: list[RecipeIngredientItemDict]
