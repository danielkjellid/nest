import pytest
from django.core.exceptions import ValidationError

from nest.audit_logs.models import LogEntry
from nest.products.tests.utils import create_product

from ..models import RecipeIngredient, RecipeIngredientItem, RecipeIngredientItemGroup
from ..services import (
    create_recipe_ingredient,
    delete_recipe_ingredient,
    create_recipe_ingredient_item_groups,
)
from . import utils
from nest.units.tests.utils import get_unit
from nest.core.exceptions import ApplicationError

pytestmark = pytest.mark.django_db


class TestRecipeIngredientsServices:
    def test_service_create_recipe_ingredient(self, django_assert_num_queries):
        """
        Test that create_ingredient service successfully creates an ingredient with
        expected output.
        """

        assert RecipeIngredient.objects.count() == 0

        product = create_product()
        with django_assert_num_queries(8):
            ingredient = create_recipe_ingredient(
                title="Test ingredient", product_id=product.id
            )

        assert RecipeIngredient.objects.count() == 1
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

    def test_service_delete_ingredient(self, django_assert_num_queries):
        """
        Test that delete_ingredient successfully deletes an ingredient and logs it.
        """

        product = create_product()
        ingredient = utils.create_recipe_ingredient(
            title="Test ingredient", product=product
        )

        assert RecipeIngredient.objects.count() == 1
        assert LogEntry.objects.count() == 0

        with django_assert_num_queries(4):
            delete_recipe_ingredient(pk=ingredient.id)

        assert RecipeIngredient.objects.filter(id=ingredient.id).first() is None
        assert LogEntry.objects.count() == 1

    def test_service_create_recipe_ingredient_item_groups(
        self, immediate_on_commit, django_assert_num_queries
    ):
        """
        Test that creating ingredient item groups using the create_ingredient_item_groups
        service works as expected within query limits.
        """

        recipe = utils.create_recipe()
        payload = [
            {
                "title": "Cod with peppers",
                "ordering": 1,
                "ingredients": [
                    {
                        "ingredient_id": utils.create_recipe_ingredient(
                            title="Green peppers",
                            product=create_product(name="Peppers, green"),
                        ).id,
                        "additional_info": None,
                        "portion_quantity": "100",
                        "portion_quantity_unit_id": get_unit("g").id,
                    },
                    {
                        "ingredient_id": utils.create_recipe_ingredient(
                            title="Cod", product=create_product(name="Fresh luxury cod")
                        ).id,
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
                        "ingredient_id": utils.create_recipe_ingredient(
                            title="Parsly",
                            product=create_product(name="Fresh parsly"),
                        ).id,
                        "additional_info": None,
                        "portion_quantity": "20",
                        "portion_quantity_unit_id": get_unit("g").id,
                    }
                ],
            },
        ]

        assert RecipeIngredientItemGroup.objects.count() == 0
        assert RecipeIngredientItem.objects.count() == 0

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
            item_groups[0]
            .ingredient_items.all()
            .values_list("ingredient__id", flat=True)
        ) == {item["ingredient_id"] for item in payload[0]["ingredients"]}

        assert item_groups[1].recipe_id == recipe.id
        assert item_groups[1].title == payload[1]["title"]
        assert item_groups[1].ordering == payload[1]["ordering"]
        assert set(
            item_groups[1]
            .ingredient_items.all()
            .values_list("ingredient__id", flat=True)
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
