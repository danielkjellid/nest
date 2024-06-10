from decimal import Decimal, ROUND_HALF_UP

import math
from pydantic import BaseModel, Field
import pandas as pd
from itertools import combinations, chain
import subprocess
import polars as pl

from nest.recipes.core.records import RecipeDetailRecord


class PlanIngredient(BaseModel):
    unit_price: Decimal
    unit_quantity: Decimal
    required_quantity: Decimal

    @property
    def total_quantity(self) -> int:
        return math.ceil(self.required_quantity / self.unit_quantity)

    @property
    def total_price(self) -> Decimal:
        return self.unit_price * self.total_quantity

    def add_quantity(self, quantity_to_add: Decimal) -> None:
        self.required_quantity += quantity_to_add


ProductId = int


class Plan(BaseModel):
    budget: Decimal
    recipes: dict[int, int]
    complete_ingredients: dict[ProductId, PlanIngredient]
    warnings: list[str]

    @property
    def remaining_budget(self) -> Decimal:
        ingredient_price = sum(
            ingredient.total_price for ingredient in self.complete_ingredients.values()
        )
        return Decimal(self.budget - ingredient_price).quantize(rounding=ROUND_HALF_UP)

    def add_recipe(self):
        ...


def run_plan_recipes_placement_distributor(recipes: list[RecipeDetailRecord]) -> Plan:
    # plan = Plan(budget=budget, recipes=[], complete_ingredients={}, warnings=[])
    product_data = []
    recipe_products = {recipe.id: [] for recipe in recipes}

    for recipe in recipes:
        for group in recipe.ingredient_item_groups:
            for item in group.ingredient_items:
                product = item.ingredient.product
                data = {
                    "recipe_id": recipe.id,
                    "product_id": product.id,
                    "name": product.full_name,
                    "unit_price": product.gross_unit_price,
                    "unit_quantity": product.unit_quantity,
                    "portion_quantity": item.portion_quantity,
                }
                recipe_products[recipe.id].append(product.id)
                product_data.append(data)

    product_df = pl.DataFrame(product_data)

    print(product_df)

    recipe_df = pl.DataFrame(
        [{"recipe_id": recipe.id, "title": recipe.title} for recipe in recipes]
    )

    print(product_df.filter(pl.col("recipe_id") == 26))

    print(recipe_df)

    # Itere gjennom og gi score basert på:
    # - fisk (om det ikke finnes andre middager med det)
    # - kostnad (kanskje basert på top occurances, da burde man gi en høyere score til
    #   oppskrifter med like produkter)
    # - ta n øverste score og se om de passer inn i constraints, hvis ikke, bytt ut
    # - den med minst score med den med høyest som passer

    # Trenger man en connection df med recipe_id, product_id, portion_quantity?
