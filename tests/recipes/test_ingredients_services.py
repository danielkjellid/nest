from decimal import Decimal
from typing import Any

import pytest
from django.core.exceptions import ValidationError

from nest.audit_logs.models import LogEntry
from nest.core.exceptions import ApplicationError
from nest.products.core.models import Product
from nest.recipes.ingredients.models import (
    RecipeIngredient,
    RecipeIngredientItemGroup,
)
from nest.recipes.ingredients.services import (
    IngredientGroupItem,
    IngredientItem,
    _get_ingredient_item_group_id,
    _validate_ingredient_item_groups,
    create_or_update_recipe_ingredient_item_groups,
    create_or_update_recipe_ingredient_items,
    create_recipe_ingredient,
    delete_recipe_ingredient,
)
from nest.recipes.steps.enums import RecipeStepType
from nest.recipes.steps.services import Step


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


@pytest.mark.recipe_ingredient_item_groups(
    group1={"title": "group1", "ordering": 1},
    group2={"title": "group2", "ordering": 2},
    group3={"title": "group3", "ordering": 3},
)
@pytest.mark.parametrize("group", ("group1", "group2", "group3"))
def test_service__get_ingredient_item_group_id(recipe_ingredient_item_groups, group):
    """
    Test that the _get_ingredient_item_group_id service util is able to find the correct
    group instance based on group item.
    """
    recipe_group = recipe_ingredient_item_groups[group]
    recipe_groups = list(recipe_ingredient_item_groups.values())

    group_id = _get_ingredient_item_group_id(
        group_item=IngredientGroupItem(
            title=recipe_group.title,
            ordering=recipe_group.ordering,
            ingredient_items=[],
        ),
        recipe_groups=recipe_groups,
    )

    # Assert that we're able to find the correct group id based on passed group item.
    assert group_id == recipe_group.id

    # If not matching group is found, generator will raise StopIteration.
    with pytest.raises(StopIteration):
        _get_ingredient_item_group_id(
            group_item=IngredientGroupItem(
                title="title does not exist",
                ordering=recipe_group.ordering,
                ingredient_items=[],
            ),
            recipe_groups=recipe_groups,
        )

    with pytest.raises(StopIteration):
        _get_ingredient_item_group_id(
            group_item=IngredientGroupItem(
                title=recipe_group.title,
                ordering=4,
                ingredient_items=[],
            ),
            recipe_groups=recipe_groups,
        )


@pytest.mark.recipe
@pytest.mark.products(
    product1={"name": "Product 1"},
    product2={"name": "Product 2"},
    product3={"name": "Product 3"},
    product4={"name": "Product 4"},
)
@pytest.mark.recipe_ingredients(
    ingredient1={"title": "Green peppers", "product": "product1"},
    ingredient2={"title": "Cod", "product": "product2"},
    ingredient3={"title": "Parsly", "product": "product3"},
    ingredient4={"title": "Tomatoes", "product": "product4"},
)
@pytest.mark.recipe_ingredient_item_groups(
    group1={"ordering": 1}, group2={"ordering": 2}, group3={"ordering": 3}
)
@pytest.mark.recipe_ingredient_items(
    item1={"ingredient_group": "group1", "ingredient": "ingredient1"},
    item2={"ingredient_group": "group2", "ingredient": "ingredient2"},
    item3={"ingredient_group": "group3", "ingredient": "ingredient3"},
)
def test_service_create_or_update_recipe_ingredient_items(
    recipe,
    recipe_ingredient_items,
    recipe_ingredients,
    get_unit,
    recipe_ingredient_item_groups,
    django_assert_num_queries,
    immediate_on_commit,
):
    grams = get_unit("g")

    group1 = recipe_ingredient_item_groups["group1"]
    group2 = recipe_ingredient_item_groups["group2"]
    group3 = recipe_ingredient_item_groups["group3"]

    assert group3.ingredient_items.count() == 1

    item1 = recipe_ingredient_items["item1"]
    item2 = recipe_ingredient_items["item2"]
    item3 = recipe_ingredient_items["item3"]

    assert item1.ingredient_group == group1
    assert item2.ingredient_group == group2
    assert item3.ingredient_group == group3

    item_to_create = IngredientItem(
        id=None,
        ingredient=recipe_ingredients["ingredient4"].id,
        portion_quantity=Decimal("100.00"),
        portion_quantity_unit=grams.id,
    )

    groups = [
        IngredientGroupItem(
            id=group1.id,
            title=group1.title,
            ordering=group1.ordering,
            ingredient_items=[
                IngredientItem(
                    id=item1.id,
                    ingredient=item1.ingredient_id,
                    portion_quantity=item1.portion_quantity,
                    portion_quantity_unit=item1.portion_quantity_unit_id,
                    additional_info=item1.additional_info,
                ),
                IngredientItem(  # Move item2 to group1
                    id=item2.id,
                    ingredient=item2.ingredient_id,
                    portion_quantity=item2.portion_quantity,
                    portion_quantity_unit=item2.portion_quantity_unit_id,
                    additional_info=item2.additional_info,
                ),
            ],
        ),
        IngredientGroupItem(
            id=group2.id,
            title=group2.title,
            ordering=group2.ordering,
            ingredient_items=[],
        ),
        IngredientGroupItem(
            id=group3.id,
            title=group3.title,
            ordering=group3.ordering,
            ingredient_items=[
                IngredientItem(
                    id=item3.id,
                    ingredient=item3.ingredient_id,
                    portion_quantity=item3.portion_quantity,
                    portion_quantity_unit=item3.portion_quantity_unit_id,
                    additional_info=item3.additional_info,
                ),
                item_to_create,
            ],
        ),
    ]

    with django_assert_num_queries(4):
        create_or_update_recipe_ingredient_items(recipe_id=recipe.id, groups=groups)

    item1.refresh_from_db()
    item2.refresh_from_db()
    item3.refresh_from_db()
    group3.refresh_from_db()

    assert item1.ingredient_group_id == group1.id
    assert item2.ingredient_group_id == group1.id
    assert item3.ingredient_group_id == group3.id

    assert group3.ingredient_items.count() == 2
    new_item = group3.ingredient_items.exclude(id=item3.id).first()

    assert new_item is not None
    assert new_item.ingredient_id == recipe_ingredients["ingredient4"].id
    assert new_item.portion_quantity == Decimal("100.00")
    assert new_item.portion_quantity_unit_id == grams.id


def test_service__validate_ingredient_item_groups():
    """
    Test that the validation function correctly raised expected exceptions.
    """
    with pytest.raises(ApplicationError):
        _validate_ingredient_item_groups(
            ingredient_group_items=[
                IngredientGroupItem(
                    id=1, title="Some title", ordering=1, ingredient_items=[]
                ),
                IngredientGroupItem(
                    id=2, title="Some other title", ordering=1, ingredient_items=[]
                ),
            ]
        )

    with pytest.raises(ApplicationError):
        _validate_ingredient_item_groups(
            ingredient_group_items=[
                IngredientGroupItem(
                    id=1, title="Same title", ordering=1, ingredient_items=[]
                ),
                IngredientGroupItem(
                    id=2, title="Same title", ordering=2, ingredient_items=[]
                ),
            ]
        )


@pytest.mark.recipe
@pytest.mark.recipe_ingredient_item_groups(group1={"ordering": 1})
def test_service_create_or_update_recipe_ingredient_item_groups(
    recipe,
    recipe_ingredient_item_groups,
    django_assert_num_queries,
    immediate_on_commit,
    mocker,
):
    """
    Test that create_or_update_recipe_ingredient_item_groups successfully creates or
    updates item groups within query limits.
    """
    recipe_ingredient_item_group = recipe_ingredient_item_groups["group1"]
    create_ingredient_items_mock = mocker.patch(
        "nest.recipes.ingredients.services.create_or_update_recipe_ingredient_items"
    )

    data = [
        IngredientGroupItem(
            id=recipe_ingredient_item_group.id,
            title="New title",
            ordering=recipe_ingredient_item_group.ordering,
            ingredient_items=[],
        ),
        IngredientGroupItem(
            id=None,
            title="Test title",
            ordering=2,
            ingredient_items=[],
        ),
    ]

    initial_group_count = RecipeIngredientItemGroup.objects.count()

    with immediate_on_commit, django_assert_num_queries(5):
        create_or_update_recipe_ingredient_item_groups(
            recipe_id=recipe.id, ingredient_item_groups=data
        )

    # A group already exists, but a new one should be created as well, bringing the
    # total up to initial_count + 1.
    assert RecipeIngredientItemGroup.objects.count() == initial_group_count + 1

    # Make sure the title has been edited successfully.
    assert recipe_ingredient_item_group.title != "New title"
    recipe_ingredient_item_group.refresh_from_db()
    assert recipe_ingredient_item_group.title == "New title"

    created_item_group = RecipeIngredientItemGroup.objects.exclude(
        id=recipe_ingredient_item_group.id
    ).first()
    created_group_ingredient_items = created_item_group.ingredient_items.all()

    assert created_item_group.title == "Test title"
    assert created_item_group.ordering == 2
    assert all(
        item.ingredient_group_id == created_item_group.id
        for item in created_group_ingredient_items
    )

    create_ingredient_items_mock.assert_called_once_with(
        recipe_id=recipe.id, groups=data
    )

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
