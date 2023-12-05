import pytest
from nest.recipes.ingredients.models import (
    RecipeIngredient,
    RecipeIngredientItem,
    RecipeIngredientItemGroup,
)
from nest.recipes.ingredients.services import (
    create_recipe_ingredient,
    delete_recipe_ingredient,
    create_recipe_ingredient_item_groups,
)
from nest.core.exceptions import ApplicationError
from nest.products.core.models import Product
from typing import Any
from django.core.exceptions import ValidationError
from nest.audit_logs.models import LogEntry


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


@pytest.mark.recipe
@pytest.mark.products(
    product_1={"name": "Peppers, green"},
    product_2={"name": "Fresh luxury cod"},
    product_3={"name": "Fresh parsly"},
)
@pytest.mark.recipe_ingredients(
    ingredient_1={"title": "Green peppers", "product": "product_1"},
    ingredient_2={"title": "Cod", "product": "product_2"},
    ingredient_3={"title": "Parsly", "product": "product_3"},
)
def test_service_create_recipe_ingredient_item_groups(
    recipe, recipe_ingredients, get_unit, immediate_on_commit, django_assert_num_queries
):
    payload = [
        {
            "title": "Cod with peppers",
            "ordering": 1,
            "ingredients": [
                {
                    "ingredient_id": recipe_ingredients["ingredient_1"].id,
                    "additional_info": None,
                    "portion_quantity": "100",
                    "portion_quantity_unit_id": get_unit("g").id,
                },
                {
                    "ingredient_id": recipe_ingredients["ingredient_2"].id,
                    "additional_info": "Descaled",
                    "portion_quantity": "1",
                    "portion_quantity_unit_id": get_unit("kg").id,
                },
            ],
        },
        {
            "title": "Accessories",
            "ordering": 2,
            "ingredients": [
                {
                    "ingredient_id": recipe_ingredients["ingredient_3"].id,
                    "additional_info": None,
                    "portion_quantity": "20",
                    "portion_quantity_unit_id": get_unit("g").id,
                }
            ],
        },
    ]

    ingredient_item_group_initial_count = RecipeIngredientItemGroup.objects.count()
    ingredient_item_initial_count = RecipeIngredientItem.objects.count()

    with immediate_on_commit, django_assert_num_queries(4):
        create_recipe_ingredient_item_groups(
            recipe_id=recipe.id, ingredient_group_items=payload
        )

    item_groups = RecipeIngredientItemGroup.objects.all().order_by("ordering")

    assert len(item_groups) == 2

    assert item_groups[0].recipe_id == recipe.id
    assert item_groups[0].title == payload[0]["title"]
    assert item_groups[0].ordering == payload[0]["ordering"]
    assert set(
        item_groups[0].ingredient_items.all().values_list("ingredient__id", flat=True)
    ) == {item["ingredient_id"] for item in payload[0]["ingredients"]}

    assert item_groups[1].recipe_id == recipe.id
    assert item_groups[1].title == payload[1]["title"]
    assert item_groups[1].ordering == payload[1]["ordering"]
    assert set(
        item_groups[1].ingredient_items.all().values_list("ingredient__id", flat=True)
    ) == {item["ingredient_id"] for item in payload[1]["ingredients"]}

    # Test that ApplicationError is raised when ordering is not unique.
    with pytest.raises(ApplicationError):
        create_recipe_ingredient_item_groups(
            recipe_id=recipe.id,
            ingredient_group_items=[
                {
                    "title": "Cod with peppers",
                    "ordering": 1,
                    "ingredients": [],
                },
                {
                    "title": "Accessories",
                    "ordering": 1,
                    "ingredients": [],
                },
            ],
        )

    # Test that ApplicationError is raised when title is not unique.
    with pytest.raises(ApplicationError):
        create_recipe_ingredient_item_groups(
            recipe_id=recipe.id,
            ingredient_group_items=[
                {
                    "title": "Cod with peppers",
                    "ordering": 1,
                    "ingredients": [],
                },
                {
                    "title": "Cod with peppers",
                    "ordering": 2,
                    "ingredients": [],
                },
            ],
        )
