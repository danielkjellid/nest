import pytest
from django.core.exceptions import ValidationError

from nest.products.tests.utils import create_product

from ..models import Ingredient
from ..services import create_ingredient

pytestmark = pytest.mark.django_db


class TestIngredientsServices:
    def test_service_create_ingredient(self, django_assert_num_queries):
        """
        Test that create_ingredient service successfully creates an ingredient with
        expected output.
        """

        assert Ingredient.objects.count() == 0

        product = create_product()
        with django_assert_num_queries(8):
            ingredient = create_ingredient(
                title="Test ingredient", product_id=product.id
            )

        assert Ingredient.objects.count() == 1
        assert ingredient.title == "Test ingredient"
        assert ingredient.product.id == product.id

        # Test that validation error is raised if we try to create another ingredient
        # with the same title.
        with pytest.raises(ValidationError):
            create_ingredient(title="Test ingredient 1", product_id=999)

        # Test that validation error is raised if we try to create another ingredient
        # with the same product.
        with pytest.raises(ValidationError):
            create_ingredient(title="Test ingredient 2", product_id=product.id)
