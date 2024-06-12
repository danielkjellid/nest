from decimal import Decimal
import polars as pl

from nest.recipes.core.records import RecipeDetailRecord


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

        self.products_df = self._get_products_dataframe()

        self.plan_recipe_ids = []

    def _get_products_dataframe(self) -> pl.DataFrame:
        product_data = []

        for recipe in self.recipes:
            for group in recipe.ingredient_item_groups:
                for item in group.ingredient_items:
                    product = item.ingredient.product
                    data = {
                        "recipe_id": recipe.id,
                        "product_id": product.id,
                        "name": product.full_name,
                        "unit_price": product.gross_unit_price,
                        "unit_quantity": product.unit_quantity,
                        "unit_abbreviation": product.unit.abbreviation,
                        "portion_quantity": item.portion_quantity,
                        "portion_quantity_unit_abbr": item.portion_quantity_unit.abbreviation,
                        "required_amount": (
                            item.portion_quantity / product.unit_quantity
                        ),
                    }
                    product_data.append(data)

        return pl.DataFrame(product_data)

    def _calculate_score_for_recipes(self):
        recipes_data = []
        score_weights = {
            "equal_products": 10,
            "pescatarian": 5,
            "vegetarian": 1,
        }

        for recipe in self.recipes:
            recipe_score = 0

            recipe_product_ids = self.products_df.filter(recipe_id=recipe.id).select(
                "product_id"
            )

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

            recipes_data.append(
                {
                    "recipe_id": recipe.id,
                    "recipe_title": recipe.title,
                    "is_pescatarian": recipe.is_pescatarian,
                    "is_vegetarian": recipe.is_vegetarian,
                    "score": recipe_score,
                }
            )

        return recipes_data

    def _create_plan(self, recipe_ids_to_exclude: list[int] | None = None):
        self.num_iterations += 1

        if self.num_iterations >= self.max_num_iterations:
            raise Exception("Unable to find an applicable plan...")

        recipe_ids_to_exclude = recipe_ids_to_exclude or []
        if len(recipe_ids_to_exclude):
            filtered_recipes = [
                recipe
                for recipe in self.recipes
                if recipe.id not in recipe_ids_to_exclude
            ]

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

        total_plan_price = (
            self.products_df.filter(
                pl.col("recipe_id").is_in(recipes_df.select("recipe_id"))
            )
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
            # Find the recipe that has the least common products with other recipes and
            # Try to re-run plan without that to maximize ingredient yield.
            least_occured_recipe_id = (
                self.products_df.filter(
                    pl.col("recipe_id").is_in(recipes_df.select("recipe_id"))
                )
                .select(pl.col("recipe_id").value_counts(sort=True).last())
                .item()["recipe_id"]
            )

            return self._create_plan(recipe_ids_to_exclude=[least_occured_recipe_id])

        return [recipe for recipe in self.recipes if recipe.id in self.plan_recipe_ids]

    def create_plan(self):
        return self._create_plan()
