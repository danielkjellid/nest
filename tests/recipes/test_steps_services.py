from datetime import timedelta

import pytest

from nest.recipes.ingredients.services import IngredientItem
from nest.recipes.steps.enums import RecipeStepType
from nest.recipes.steps.models import RecipeStep
from nest.recipes.steps.services import Step, create_or_update_recipe_steps


@pytest.mark.recipe
@pytest.mark.products(
    product1={"name": "Product 1"},
    product2={"name": "Product 2"},
    product3={"name": "Product 3"},
)
@pytest.mark.recipe_ingredients(
    ingredient1={"title": "Green peppers", "product": "product1"},
    ingredient2={"title": "Cod", "product": "product2"},
    ingredient3={"title": "Parsly", "product": "product3"},
)
@pytest.mark.recipe_steps(step1={"number": 1})
@pytest.mark.recipe_ingredient_item_groups(
    group1={"ordering": 1}, group2={"ordering": 2}, group3={"ordering": 3}
)
@pytest.mark.recipe_ingredient_items(
    item1={"ingredient_group": "group1", "step": "step1", "ingredient": "ingredient1"},
    item2={"ingredient_group": "group2", "step": None, "ingredient": "ingredient2"},
    item3={"ingredient_group": "group3", "step": None, "ingredient": "ingredient3"},
)
def test_service_create_or_update_recipe_steps(
    recipe,
    recipe_steps,
    recipe_ingredient_items,
    django_assert_num_queries,
    immediate_on_commit,
):
    recipe_step = recipe_steps["step1"]

    item1 = recipe_ingredient_items["item1"]
    item2 = recipe_ingredient_items["item2"]
    item3 = recipe_ingredient_items["item3"]

    new_duration = 6

    assert recipe_step.duration != timedelta(minutes=new_duration)

    data = [
        Step(
            id=recipe_step.id,
            number=recipe_step.number,
            duration=new_duration,
            instruction=recipe_step.instruction,
            step_type=recipe_step.step_type,
            ingredient_items=[
                IngredientItem(
                    id=item1.id,
                    ingredient=item1.ingredient_id,
                    portion_quantity=item1.portion_quantity,
                    portion_quantity_unit=item1.portion_quantity_unit.id,
                    additional_info=item1.additional_info,
                )
            ],
        ),
        Step(
            id=None,
            number=2,
            duration=5,
            instruction="Some sample instruction",
            step_type=RecipeStepType.PREPARATION,
            ingredient_items=[
                IngredientItem(
                    id=item2.id,
                    ingredient=item2.ingredient_id,
                    portion_quantity=item2.portion_quantity,
                    portion_quantity_unit=item2.portion_quantity_unit.id,
                    additional_info=item2.additional_info,
                ),
                IngredientItem(
                    id=item3.id,
                    ingredient=item3.ingredient_id,
                    portion_quantity=item3.portion_quantity,
                    portion_quantity_unit=item3.portion_quantity_unit.id,
                    additional_info=item3.additional_info,
                ),
            ],
        ),
    ]

    initial_step_count = RecipeStep.objects.count()

    with immediate_on_commit, django_assert_num_queries(7):
        create_or_update_recipe_steps(recipe_id=recipe.id, steps=data)

    # A step already exists, but a new one should be created as well, bringing the total
    # up to initial_count + 1.
    assert RecipeStep.objects.count() == initial_step_count + 1

    recipe_step.refresh_from_db()

    assert recipe_step.duration == timedelta(minutes=new_duration)
