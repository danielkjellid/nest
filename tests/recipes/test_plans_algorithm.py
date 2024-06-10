import pytest
from decimal import Decimal

from nest.recipes.plans.algorithm import (
    PlanIngredient,
    run_plan_recipes_placement_distributor,
)


def test_plan_ingredient_add_quantity():
    plan_ingredient1_price = Decimal("100.00")
    plan_ingredient1_quantity = Decimal("500.00")
    plan_ingredient1 = PlanIngredient(
        unit_price=plan_ingredient1_price,
        unit_quantity=plan_ingredient1_quantity,
        required_quantity=plan_ingredient1_quantity,
    )

    quantity_to_add = Decimal("200.00")

    plan_ingredient1.add_quantity(quantity_to_add=quantity_to_add)

    assert plan_ingredient1.total_quantity == 2
    assert plan_ingredient1.total_price == 2 * plan_ingredient1_price
