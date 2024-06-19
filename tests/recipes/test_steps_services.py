from datetime import timedelta

import pytest

from nest.recipes.ingredients.models import RecipeIngredientItem
from nest.recipes.ingredients.services import IngredientItem
from nest.recipes.steps.enums import RecipeStepType
from nest.recipes.steps.models import RecipeStep
from nest.recipes.steps.services import (
    Step,
    create_or_update_recipe_steps,
    _find_step_id_for_step_item,
    _find_ingredient_item_id_for_step_item,
)


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
    item1={"ingredient_group": "group1", "ingredient": "ingredient1"},
    item2={"ingredient_group": "group2", "ingredient": "ingredient2"},
    item3={"ingredient_group": "group3", "ingredient": "ingredient3"},
)
def test_service_create_or_update_recipe_steps(
    recipe,
    recipe_steps,
    recipe_ingredient_items,
    django_assert_num_queries,
    immediate_on_commit,
    mocker,
):
    recipe_step = recipe_steps["step1"]

    item1 = recipe_ingredient_items["item1"]
    item2 = recipe_ingredient_items["item2"]
    item3 = recipe_ingredient_items["item3"]

    create_ingredient_items_mock = mocker.patch(
        "nest.recipes.steps.services.create_or_update_recipe_step_ingredient_items"
    )

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

    with immediate_on_commit, django_assert_num_queries(4):
        create_or_update_recipe_steps(recipe_id=recipe.id, steps=data)

    # A step already exists, but a new one should be created as well, bringing the total
    # up to initial_count + 1.
    assert RecipeStep.objects.count() == initial_step_count + 1

    recipe_step.refresh_from_db()

    assert recipe_step.duration == timedelta(minutes=new_duration)

    create_ingredient_items_mock.assert_called_once_with(
        recipe_id=recipe.id, steps=data
    )


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
@pytest.mark.recipe_ingredient_items(
    item1={"ingredient": "ingredient1"},
    item2={"ingredient": "ingredient2"},
    item3={"ingredient": "ingredient3"},
)
@pytest.mark.parametrize("item", ("item1", "item2", "item3", "other"))
def test__find_ingredient_item_id_for_step_item(
    item, recipe_ingredient_items, django_assert_num_queries
):
    """
    Test that the _find_ingredient_item_id_for_step_item service util is able to find
    the correct ingredient item id for a given ingredient item.
    """
    default_item = recipe_ingredient_items["item1"]
    current_item = recipe_ingredient_items[item] if item != "other" else None

    item_id = getattr(current_item, "id", None)  # Default None - important!
    ingredient_id = getattr(current_item, "ingredient_id", default_item.ingredient_id)
    portion_quantity = getattr(
        current_item, "portion_quantity", default_item.portion_quantity
    )
    portion_quantity_unit_id = getattr(
        current_item, "portion_quantity_unit_id", default_item.portion_quantity_unit_id
    )
    additional_info = getattr(
        current_item, "additional_info", default_item.additional_info
    )

    db_items = list(RecipeIngredientItem.objects.all())

    with django_assert_num_queries(0):
        found_item_id = _find_ingredient_item_id_for_step_item(
            item=IngredientItem(
                id=item_id,
                ingredient=ingredient_id,
                portion_quantity=portion_quantity,
                portion_quantity_unit=portion_quantity_unit_id,
                additional_info=additional_info,
            ),
            recipe_ingredient_items=db_items,
        )

    # In the run with "other", we do not send in the id, to see if we're able to find
    # the item based on the given mapping (which is a copy of the default_step attrs)
    if item == "other":
        assert found_item_id == default_item.id
    else:
        assert found_item_id == current_item.id

    with pytest.raises(StopIteration):
        _find_ingredient_item_id_for_step_item(
            item=IngredientItem(
                id=None,
                ingredient=999,
                portion_quantity=10,
                portion_quantity_unit=portion_quantity_unit_id,
                additional_info=additional_info,
            ),
            recipe_ingredient_items=db_items,
        )


@pytest.mark.recipe_steps(
    step1={"number": 1},
    step2={"number": 2},
    step3={"number": 3},
)
@pytest.mark.parametrize("step", ("step1", "step2", "step3", "other"))
def test__find_step_id_for_step_item(
    step,
    recipe_steps,
    recipe_ingredient_items,
    django_assert_num_queries,
):
    """
    Test that the _find_step_id_for_step_item service util is able to find the correct
    step instance based on given item.
    """

    default_step = recipe_steps["step1"]
    current_step = recipe_steps[step] if step != "other" else None

    step_id = getattr(current_step, "id", None)  # Default None - important!
    number = getattr(current_step, "number", default_step.number)
    duration_in_minutes = (
        getattr(current_step, "duration", default_step.duration).seconds / 60
    )
    instruction = getattr(current_step, "instruction", default_step.instruction)
    step_type = getattr(current_step, "step_type", default_step.step_type).value

    db_steps = list(RecipeStep.objects.all())

    with django_assert_num_queries(0):
        found_step_id = _find_step_id_for_step_item(
            step=Step(
                id=step_id,
                number=number,
                duration=duration_in_minutes,
                instruction=instruction,
                step_type=step_type,
                ingredient_items=[],
            ),
            recipe_steps=db_steps,
        )

    # In the run with "other", we do not send in the id, to see if we're able to find
    # the step based on the given mapping (which is a copy of the default_step attrs)
    if step == "other":
        assert found_step_id == default_step.id
    else:
        assert found_step_id == current_step.id

    with pytest.raises(StopIteration):
        _find_step_id_for_step_item(
            step=Step(
                id=None,
                number=99999,
                duration=12343123,
                instruction="This step does not exist",
                step_type=step_type,
                ingredient_items=[],
            ),
            recipe_steps=db_steps,
        )


def test_service_create_or_update_recipe_step_ingredient_items():
    assert False
