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


class Distributor:
    def __init__(
        self,
        budget: Decimal,
        total_num_recipes: int,
        num_pescatarian: int,
        num_vegetarian: int,
        applicable_recipes: list[RecipeDetailRecord],
    ) -> None:
        self.budget = budget
        self.total_num_recipes = total_num_recipes
        self.num_pescatarian = num_pescatarian
        self.num_vegetarian = num_vegetarian
        self.recipes = applicable_recipes
        self.num_iterations = 0
        self.max_num_iterations = 20

    def _get_products_dataframe(self) -> pl.DataFrame:
        product_data = []

        for recipe in self.recipes:
            for group in recipe.ingredient_item_groups:
                for item in group.ingredient_items:
                    product = item.ingredient.product
                    data = {
                        "product_id": product.id,
                        "name": product.full_name,
                        "unit_price": product.gross_unit_price,
                        "unit_quantity": product.unit_quantity,
                        "unit_abbreviation": product.unit.abbreviation,
                    }
                    product_data.append(data)

        return pl.DataFrame(product_data)

    def _get_recipe_products_connection_dataframe(self) -> pl.DataFrame:
        recipe_product_connection_data = []

        for recipe in self.recipes:
            for group in recipe.ingredient_item_groups:
                for item in group.ingredient_items:
                    product = item.ingredient.product
                    data = {
                        "recipe_id": recipe.id,
                        "product_id": product.id,
                        "portion_quantity": item.portion_quantity,
                        "portion_quantity_unit_abbr": item.portion_quantity_unit.abbreviation,
                        "required_amount": (
                            item.portion_quantity / product.unit_quantity
                        ),
                    }
                    recipe_product_connection_data.append(data)

        return pl.DataFrame(recipe_product_connection_data)

    def _calculate_score_for_recipes(self):
        ...

    def create_plan(self):
        products_df = self._get_products_dataframe()
        recipe_products_df = self._get_recipe_products_connection_dataframe()

        recipes_data = []

        # Calculate score
        for recipe in self.recipes:
            recipe_score = 0
            score_weights = {"equal_products": 10, "pescatarian": 5, "vegetarian": 1}

            recipe_product_ids = recipe_products_df.filter(recipe_id=recipe.id).select(
                pl.col("product_id")
            )

            related_recipes = recipe_products_df.filter(
                (pl.col("recipe_id") != recipe.id)
                & (pl.col("product_id").is_in(recipe_product_ids))
            )

            # Count amount of products used in this recipe, which is also used in other
            # recipes.
            similar_products_count = (
                related_recipes.select(pl.col("product_id")).count().item()
            )

            recipe_score += similar_products_count * score_weights["equal_products"]

            # num_pescatarian_recipes_added = len(
            #     [
            #         data
            #         for data in recipes_data
            #         if data.get("is_pescatarian", False) is True
            #     ]
            # )
            #
            # if (
            #     self.num_pescatarian
            #     and num_pescatarian_recipes_added <= self.num_pescatarian
            #     and recipe.is_pescatarian
            # ):
            #     recipe_score += score_weights["pescatarian"]
            #
            # num_vegeterian_recipes_added = len(
            #     [
            #         data
            #         for data in recipes_data
            #         if data.get("is_pescatarian", False) is True
            #     ]
            # )
            #
            # if (
            #     self.num_vegetarian
            #     and num_vegeterian_recipes_added <= self.num_vegetarian
            #     and recipe.is_vegetarian
            # ):
            #     recipe_score += score_weights["vegetarian"]

            # Find the total cost of a recipe by calculating required amount unit price
            # across dataframes.
            recipe_cost = (
                products_df.filter(pl.col("product_id").is_in(recipe_product_ids))
                .join(
                    recipe_products_df.filter(recipe_id=recipe.id),
                    on=pl.col("product_id"),
                )
                .unique()
                .with_columns(
                    (
                        pl.col("unit_price")
                        * pl.col("required_amount").cast(pl.Float64).ceil()
                    ).alias("total_price")
                )
                .select(pl.sum("total_price"))
                .item()
            )

            recipes_data.append(
                {
                    "recipe_id": recipe.id,
                    "recipe_title": recipe.title,
                    "score": recipe_score,
                    "cost": recipe_cost,
                }
            )

        recipes_df = (
            pl.DataFrame(recipes_data)
            .sort(by="score", descending=True)
            .slice(0, self.total_num_recipes)
        )

        complete_recipe_products = []
        products_df.filter(pl.col("product_id"))

        # Calculate price - how? Do we have to list dependencies? Re-run if recipes does not fit into budget excluding one of the recipes?

        print(recipes_df)

        # Once num recipes is selected, go through and see if we can save some by combining recipe products

        # if selected_plan is over budget, find most expensive recipe an try to rerun

        print(recipes_data)
