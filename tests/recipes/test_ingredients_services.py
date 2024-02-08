from decimal import Decimal
from typing import Any

import pytest
from django.core.exceptions import ValidationError

from nest.audit_logs.models import LogEntry
from nest.core.exceptions import ApplicationError
from nest.products.core.models import Product
from nest.recipes.ingredients.models import (
    RecipeIngredient,
    RecipeIngredientItem,
    RecipeIngredientItemGroup,
)
from nest.recipes.ingredients.services import (
    IngredientGroupItem,
    IngredientItem,
    create_or_update_recipe_ingredient_item_groups,
    create_recipe_ingredient,
    delete_recipe_ingredient,
)


@pytest.mark.product
def test_service_create_recipe_ingredient(
    product: Product, django_assert_num_queries: Any
) -> None:
    """
    Test that create_ingredient service successfully creates an ingredient with
    expected output.
    """

    initial_count = RecipeIngredient.objects.count()

    with django_assert_num_queries(8):
        ingredient = create_recipe_ingredient(
            title="Test ingredient", product_id=product.id
        )

    assert RecipeIngredient.objects.count() == initial_count + 1
    assert ingredient.title == "Test ingredient"
    assert ingredient.product.id == product.id

    # Test that validation error is raised if we try to create another ingredient
    # with the same title.
    with pytest.raises(ValidationError):
        create_recipe_ingredient(title="Test ingredient 1", product_id=999)

    # Test that validation error is raised if we try to create another ingredient
    # with the same product.
    with pytest.raises(ValidationError):
        create_recipe_ingredient(title="Test ingredient 2", product_id=product.id)


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
@pytest.mark.recipe_ingredient_item_groups(group1={"ordering": 1})
@pytest.mark.recipe_ingredient_item(ingredient_group="group1", ingredient="ingredient1")
def test_service__create_or_update_recipe_ingredient_item_groups(
    recipe,
    recipe_ingredient_item_group,
    recipe_ingredient_item,
    recipe_ingredients,
    django_assert_num_queries,
    get_unit,
    immediate_on_commit,
):
    unit = get_unit("kg")

    assert recipe_ingredient_item.portion_quantity_unit != unit

    data = [
        IngredientGroupItem(
            id=recipe_ingredient_item_group.id,
            title="New title",
            ordering=recipe_ingredient_item_group.ordering,
            ingredient_items=[
                IngredientItem(
                    id=recipe_ingredient_item.id,
                    ingredient=recipe_ingredient_item.ingredient_id,
                    portion_quantity=recipe_ingredient_item.portion_quantity,
                    portion_quantity_unit=unit.id,
                    additional_info=recipe_ingredient_item.additional_info,
                )
            ],
        ),
        IngredientGroupItem(
            id=None,
            title="Test title",
            ordering=2,
            ingredient_items=[
                IngredientItem(
                    id=None,
                    ingredient=recipe_ingredients["ingredient2"].id,
                    portion_quantity="100",
                    portion_quantity_unit=unit.id,
                    additional_info=None,
                ),
                IngredientItem(
                    id=None,
                    ingredient=recipe_ingredients["ingredient3"].id,
                    portion_quantity="120",
                    portion_quantity_unit=unit.id,
                    additional_info="Some additional info",
                ),
            ],
        ),
    ]

    initial_group_count = RecipeIngredientItemGroup.objects.count()
    initial_item_count = RecipeIngredientItem.objects.count()

    with immediate_on_commit, django_assert_num_queries(9):
        create_or_update_recipe_ingredient_item_groups(
            recipe_id=recipe.id, ingredient_item_groups=data
        )

    # A group already exists, but a new one should be created as well, bringing the
    # total up to initial_count + 1.
    assert RecipeIngredientItemGroup.objects.count() == initial_group_count + 1
    # An item already exists, but two new ones should be created as well, bringing the
    # total up to initial_count + 2.
    assert RecipeIngredientItem.objects.count() == initial_item_count + 2

    # Make sure the title has been edited successfully.
    assert recipe_ingredient_item_group.title != "New title"
    recipe_ingredient_item_group.refresh_from_db()
    assert recipe_ingredient_item_group.title == "New title"
    assert recipe_ingredient_item_group.ingredient_items.count() == 1
    existing_group_ingredient_item = recipe_ingredient_item_group.ingredient_items.all()

    created_item_group = RecipeIngredientItemGroup.objects.exclude(
        id=recipe_ingredient_item_group.id
    ).first()
    created_group_ingredient_items = created_item_group.ingredient_items.all()

    assert created_item_group.title == "Test title"
    assert created_item_group.ordering == 2
    assert created_item_group.ingredient_items.count() == 2
    assert all(
        item.ingredient_group_id == created_item_group.id
        for item in created_group_ingredient_items
    )

    def get_item_for_ingredient(ingredient_id):
        return next(
            (
                item
                for item in (
                    list(created_group_ingredient_items)
                    + list(existing_group_ingredient_item)
                )
                if item.ingredient_id == ingredient_id
            ),
            None,
        )

    ingredient1_item = get_item_for_ingredient(recipe_ingredients["ingredient1"].id)
    assert ingredient1_item is not None
    assert ingredient1_item.portion_quantity == recipe_ingredient_item.portion_quantity
    # Unit should have been updated.
    assert (
        ingredient1_item.portion_quantity_unit
        != recipe_ingredient_item.portion_quantity_unit
    )
    assert ingredient1_item.portion_quantity_unit == unit
    assert ingredient1_item.additional_info == recipe_ingredient_item.additional_info

    ingredient2_item = get_item_for_ingredient(recipe_ingredients["ingredient2"].id)
    assert ingredient2_item is not None
    assert ingredient2_item.portion_quantity == Decimal("100.00")
    assert ingredient2_item.portion_quantity_unit == unit
    assert ingredient2_item.additional_info is None

    ingredient3_item = get_item_for_ingredient(recipe_ingredients["ingredient3"].id)
    assert ingredient3_item is not None
    assert ingredient3_item.portion_quantity == Decimal("120.00")
    assert ingredient3_item.portion_quantity_unit == unit
    assert ingredient3_item.additional_info == "Some additional info"

    # Test that ApplicationError is raised when ordering is not unique.
    with pytest.raises(ApplicationError):
        create_or_update_recipe_ingredient_item_groups(
            recipe_id=recipe.id,
            ingredient_item_groups=[
                IngredientGroupItem(title="Title 1", ordering=1, ingredient_items=[]),
                IngredientGroupItem(title="Title 2", ordering=1, ingredient_items=[]),
            ],
        )
        assert RecipeIngredientItemGroup.objects.count() == initial_group_count
        assert RecipeIngredientItem.objects.count() == initial_item_count

    # Test that ApplicationError is raised when title is not unique.
    with pytest.raises(ApplicationError):
        create_or_update_recipe_ingredient_item_groups(
            recipe_id=recipe.id,
            ingredient_item_groups=[
                IngredientGroupItem(title="Title 1", ordering=1, ingredient_items=[]),
                IngredientGroupItem(title="Title 1", ordering=2, ingredient_items=[]),
            ],
        )
        assert RecipeIngredientItemGroup.objects.count() == initial_group_count
        assert RecipeIngredientItem.objects.count() == initial_item_count


@pytest.mark.recipe_ingredient
def test_service_delete_recipe_ingredient(
    recipe_ingredient: RecipeIngredient, django_assert_num_queries: Any
) -> None:
    """
    Test that delete_ingredient successfully deletes an ingredient and logs it.
    """

    initial_log_count = LogEntry.objects.count()

    assert RecipeIngredient.objects.filter(id=recipe_ingredient.id).first() is not None

    with django_assert_num_queries(4):
        delete_recipe_ingredient(pk=recipe_ingredient.id)

    assert RecipeIngredient.objects.filter(id=recipe_ingredient.id).first() is None
    assert LogEntry.objects.count() == initial_log_count + 1
