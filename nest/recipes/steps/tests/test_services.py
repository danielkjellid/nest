import pytest

from nest.core.exceptions import ApplicationError
from nest.products.core.tests.utils import create_product
from nest.recipes.core.tests.utils import create_recipe
from nest.recipes.ingredients.tests.utils import (
    create_recipe_ingredient,
    create_recipe_ingredient_item,
    create_recipe_ingredient_item_group,
)
from nest.units.tests.utils import get_unit

from ..models import RecipeStep
from ..services import create_recipe_steps

pytestmark = pytest.mark.django_db


class TestRecipeStepsServices:
    def test_service_create_recipe_steps(self, django_assert_num_queries):
        """
        Test that creating steps using the create_recipe_steps service works as expected
        within query limits.
        """
        recipe = create_recipe()
        item_group_1 = create_recipe_ingredient_item_group(
            title="Cod with peppers", recipe=recipe
        )
        item_group_2 = create_recipe_ingredient_item_group(
            title="Accessories", recipe=recipe
        )
        unit = get_unit("g")

        ingredient_item1 = create_recipe_ingredient_item(
            ingredient_group=item_group_1,
            portion_quantity=150,
            portion_quantity_unit="g",
            ingredient=create_recipe_ingredient(
                title="Green peppers",
                product=create_product(name="Peppers, green"),
            ),
        )
        ingredient_item2 = create_recipe_ingredient_item(
            ingredient_group=item_group_1,
            portion_quantity=200,
            portion_quantity_unit="g",
            ingredient=create_recipe_ingredient(
                title="Cod",
                product=create_product(name="Fresh luxury cod"),
            ),
        )
        ingredient_item3 = create_recipe_ingredient_item(
            ingredient_group=item_group_2,
            portion_quantity=190,
            portion_quantity_unit="g",
            ingredient=create_recipe_ingredient(
                title="Parsly",
                product=create_product(name="Fresh parsly"),
            ),
        )
        ingredient_item4 = create_recipe_ingredient_item(
            ingredient_group=item_group_2,
            portion_quantity=100,
            portion_quantity_unit="g",
            ingredient=create_recipe_ingredient(
                title="Salt",
                product=create_product(name="Kosher salt"),
            ),
        )

        payload = [
            {
                "number": 1,
                "duration": 5,
                "instruction": "Some instruction for step 1",
                "step_type": "cooking",
                "ingredient_items": [
                    {
                        "ingredient_id": ingredient_item1.ingredient_id,
                        "portion_quantity": "150",
                        "portion_quantity_unit_id": unit.id,
                        "additional_info": None,
                    },
                    {
                        "ingredient_id": ingredient_item2.ingredient_id,
                        "portion_quantity": "200",
                        "portion_quantity_unit_id": unit.id,
                        "additional_info": None,
                    },
                    {
                        "ingredient_id": ingredient_item3.ingredient_id,
                        "portion_quantity": "190",
                        "portion_quantity_unit_id": unit.id,
                        "additional_info": None,
                    },
                ],
            },
            {
                "number": 2,
                "duration": 3,
                "instruction": "Some instruction for step 2",
                "step_type": "cooking",
                "ingredient_items": [
                    {
                        "ingredient_id": ingredient_item4.ingredient_id,
                        "portion_quantity": "100",
                        "portion_quantity_unit_id": unit.id,
                        "additional_info": None,
                    },
                ],
            },
        ]

        assert RecipeStep.objects.count() == 0

        with django_assert_num_queries(3):
            create_recipe_steps(recipe_id=recipe.id, steps=payload)

        recipe_steps = RecipeStep.objects.all().order_by("number")

        assert len(recipe_steps) == 2

        assert recipe_steps[0].recipe_id == recipe.id
        assert recipe_steps[0].number == payload[0]["number"]
        assert recipe_steps[0].instruction == payload[0]["instruction"]
        assert set(
            recipe_steps[0].ingredient_items.all().values_list("id", flat=True)
        ) == {ingredient_item1.id, ingredient_item2.id, ingredient_item3.id}

        assert recipe_steps[1].recipe_id == recipe.id
        assert recipe_steps[1].number == payload[1]["number"]
        assert recipe_steps[1].instruction == payload[1]["instruction"]
        assert set(
            recipe_steps[1].ingredient_items.all().values_list("id", flat=True)
        ) == {ingredient_item4.id}

        # Test that application error is raised if number is off sequence.
        with pytest.raises(ApplicationError):
            create_recipe_steps(
                recipe_id=recipe.id,
                steps=[
                    {
                        "number": 1,
                        "duration": 1,
                        "instruction": "Some instruction",
                        "step_type": "cooking",
                        "ingredient_items": [],
                    },
                    {
                        "number": 3,
                        "duration": 1,
                        "instruction": "Some instruction",
                        "step_type": "cooking",
                        "ingredient_items": [],
                    },
                ],
            )

        # Test that ApplicationError is raised if number: 1 is not present in payload.
        with pytest.raises(ApplicationError):
            create_recipe_steps(
                recipe_id=recipe.id,
                steps=[
                    {
                        "number": 2,
                        "duration": 1,
                        "instruction": "Some instruction",
                        "step_type": "cooking",
                        "ingredient_items": [],
                    },
                    {
                        "number": 3,
                        "duration": 1,
                        "instruction": "Some instruction",
                        "step_type": "cooking",
                        "ingredient_items": [],
                    },
                ],
            )

        # Test that ApplicationError is raised if any of the instructions is empty.
        with pytest.raises(ApplicationError):
            create_recipe_steps(
                recipe_id=recipe.id,
                steps=[
                    {
                        "number": 1,
                        "duration": 1,
                        "instruction": "",
                        "step_type": "cooking",
                        "ingredient_items": [],
                    },
                    {
                        "number": 1,
                        "duration": 1,
                        "instruction": "Some instruction",
                        "step_type": "cooking",
                        "ingredient_items": [],
                    },
                ],
            )
