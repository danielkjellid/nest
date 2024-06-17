from decimal import Decimal
from typing import TypedDict

import polars as pl

from nest.core.exceptions import ApplicationError
from nest.recipes.core.records import RecipeDetailRecord
from nest.units.utils import convert_unit_quantity


class RecipeScoreData(TypedDict, total=True):
    recipe_id: int
    is_vegetarian: bool
    is_pescatarian: bool
    score: int


class PlanDistributor:
    def __init__(
        self,
        budget: Decimal,
        total_num_recipes: int,
        num_portions_per_recipe: int,
        num_pescatarian: int,
        num_vegetarian: int,
        applicable_recipes: list[RecipeDetailRecord],
    ) -> None:
        self.budget = budget
        self.total_num_recipes = total_num_recipes
        self.num_portions_per_recipe = num_portions_per_recipe
        self.num_pescatarian = num_pescatarian
        self.num_vegetarian = num_vegetarian
        self.recipes = applicable_recipes
        self.num_iterations = 0
        self.max_num_iterations = 20

        self.products_df = self._get_products_dataframe()

        self.plan_recipe_ids: list[int] = []

    def _get_products_dataframe(self) -> pl.DataFrame:
        """
        Create pl.DataFrame containing product and ingredient data.
        """
        product_data = []

        for recipe in self.recipes:
            recipe_portion_factor = Decimal(
                self.num_portions_per_recipe / recipe.default_num_portions
            ).quantize(Decimal("1.0"))

            for group in recipe.ingredient_item_groups:
                for item in group.ingredient_items:
                    product = item.ingredient.product

                    portion_quantity = item.portion_quantity * recipe_portion_factor

                    converted_quantity = convert_unit_quantity(
                        quantity=portion_quantity,
                        from_unit=item.portion_quantity_unit,
                        to_unit=product.unit,
                        piece_weight=product.unit_quantity,
                    )

                    if converted_quantity is None or product.unit_quantity is None:
                        raise ApplicationError(
                            "Recipe or product is missing quantity, impossible to "
                            "calculate required quantity without it",
                            extra={"product_id": product.id},
                        )

                    data = {
                        "recipe_id": recipe.id,
                        "product_id": product.id,
                        "name": product.full_name,
                        "unit_price": product.gross_unit_price,
                        "unit_quantity": product.unit_quantity,
                        "unit_abbreviation": product.unit.abbreviation,
                        "portion_quantity": item.portion_quantity,
                        "portion_quantity_unit_abbr": item.portion_quantity_unit.abbreviation,
                        "required_amount": converted_quantity / product.unit_quantity,
                    }
                    product_data.append(data)

        return pl.DataFrame(product_data)

    def _calculate_score_for_recipes(self) -> list[RecipeScoreData]:
        """
        Calculate a pleminiray score for all recipes based on common products used,
        pescatarian and vegetarian.
        """
        recipes_data: list[RecipeScoreData] = []
        score_weights = {
            "equal_products": 10,
            "pescatarian": 5,
            "vegetarian": 1,
            "num_usages": -3,  # Punish recipes that's often used in plans.
        }

        for recipe in self.recipes:
            recipe_score = 0

            # Get a frame of product ids associated with the current iteration.
            recipe_product_ids = self.products_df.filter(
                recipe_id=recipe.id
            ).get_column("product_id")

            # Count amount of products used in this recipe, which is also used in other
            # recipes.
            similar_products_count = (
                self.products_df.filter(
                    (pl.col("recipe_id") != recipe.id)
                    & (pl.col("product_id").is_in(recipe_product_ids))
                )
                .select("product_id")
                .count()
                .item()
            )

            # Add score base on similarities with other producuts.
            # Pitfall: commonalities like butter, oil etc. Maybe ok?
            recipe_score += similar_products_count * score_weights["equal_products"]

            num_pescatarian_recipes_added = len(
                [d for d in recipes_data if d.get("is_pescatarian", False) is True]
            )

            if (
                self.num_pescatarian
                and num_pescatarian_recipes_added <= self.num_pescatarian
                and recipe.is_pescatarian
            ):
                recipe_score += score_weights["pescatarian"]

            num_vegeterian_recipes_added = len(
                [d for d in recipes_data if d.get("is_vegetarian", False) is True]
            )

            if (
                self.num_vegetarian
                and num_vegeterian_recipes_added <= self.num_vegetarian
                and recipe.is_vegetarian
            ):
                recipe_score += score_weights["vegetarian"]

            recipe_score += recipe.num_plan_usages * score_weights["num_usages"]

            recipes_data.append(
                RecipeScoreData(
                    recipe_id=recipe.id,
                    is_pescatarian=recipe.is_pescatarian,
                    is_vegetarian=recipe.is_vegetarian,
                    score=recipe_score,
                )
            )

        return recipes_data

    def create_plan(
        self, recipe_ids_to_exclude: list[int] | None = None
    ) -> list[RecipeDetailRecord]:
        """
        Attempt to create the recipe plan itself.
        """

        # Bump num to keep track of iterations made.
        self.num_iterations += 1

        # If we've spent the allowed total iterations and still have not found an
        # applicable plan, we give up.
        if self.num_iterations >= self.max_num_iterations:
            raise Exception("Unable to find an applicable plan...")

        # Filter out recipe ids we want to exclude from the current and subsequent
        # iterations. We attempt to create the plan requirively, which also menas that
        # we're filtering recursively. Might have to rethink this as it severely narrows
        # down options the further down the chain you go, but maybe it's alright?
        recipe_ids_to_exclude = recipe_ids_to_exclude or []
        if len(recipe_ids_to_exclude):
            filtered_recipes = [
                recipe
                for recipe in self.recipes
                if recipe.id not in recipe_ids_to_exclude
            ]

            # No more recipes to attempt to create plan from, give up.
            if not len(filtered_recipes):
                raise Exception("Unable to find any applicable plan...")

            self.recipes = filtered_recipes

        recipes_data = self._calculate_score_for_recipes()

        # Convert recipes into a dataframe and get the top n (total_num_recipes) with
        # the highest scores.
        recipes_df = (
            pl.DataFrame(recipes_data)
            .sort(by="score", descending=True)
            .slice(0, self.total_num_recipes)
        )

        recipes_df_ids = recipes_df.get_column("recipe_id")

        # Calculate the total plan price by combining ingredients from all recipes being
        # evaluated. E.g. if recipe 1 needs 0,5 cheese, and recipe 2 needs 0,5 cheese,
        # we aggregate these into requiring 1 cheese in total, and thereafter
        # calculating the price.
        total_plan_price = (
            self.products_df.filter(pl.col("recipe_id").is_in(recipes_df_ids))
            .select(
                [
                    "recipe_id",
                    "product_id",
                    "unit_price",
                    "required_amount",
                ]
            )
            .groupby(["product_id", "unit_price"])
            .agg(
                [
                    pl.col("required_amount").sum(),
                    pl.col("recipe_id").alias("recipes").unique(),
                ]
            )
            .with_columns(
                (
                    "unit_price" * pl.col("required_amount").cast(pl.Float64).ceil()
                ).alias("total_price")
            )
            .select("total_price")
            .sum()
        ).item()

        if total_plan_price <= self.budget:
            # If we're within budget, get the ids from the recipes_df, do a sanity check
            # and populate the plan_recipe_ids list.
            recipe_ids = (
                recipes_df.select([pl.col("recipe_id")])
                .get_column("recipe_id")
                .to_list()
            )

            if len(recipe_ids) != self.total_num_recipes:
                raise Exception(
                    "Something went wrong, we found more or less recipes than we were "
                    "supposed to."
                )

            self.plan_recipe_ids = recipe_ids

        else:
            # We're not within budget and have to re-iterate on the solution. Find the
            # recipe that has the least common products with other recipes and try to
            # re-run plan without that to avoid affecting the planned recipe list too
            # much.
            least_occured_recipe_id = (
                self.products_df.filter(pl.col("recipe_id").is_in(recipes_df_ids))
                .select(pl.col("recipe_id").value_counts(sort=True).last())
                .item()["recipe_id"]
            )

            # Recurisvely try to create plan without the least occured recipe.
            return self.create_plan(recipe_ids_to_exclude=[least_occured_recipe_id])

        return [recipe for recipe in self.recipes if recipe.id in self.plan_recipe_ids]
