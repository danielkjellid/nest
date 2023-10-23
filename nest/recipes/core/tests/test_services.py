import pytest

from ..enums import RecipeDifficulty, RecipeStatus
from ..models import Recipe
from ..services import create_recipe

pytestmark = pytest.mark.django_db


class TestRecipeCoreServices:
    def test_service_create_recipe(self, django_assert_num_queries):
        """
        Test that the create_recipe service successfully creates a recipe with expected
        output.
        """

        assert Recipe.objects.count() == 0

        fields = {
            "title": "A new recipe",
            "default_num_portions": 3,
            "status": "draft",
            "difficulty": "medium",
            "is_vegetarian": True,
        }

        with django_assert_num_queries(3):
            recipe = create_recipe(**fields)

        assert Recipe.objects.count() == 1

        assert recipe.title == fields["title"]
        assert recipe.default_num_portions == fields["default_num_portions"]
        assert recipe.status == RecipeStatus.DRAFT
        assert recipe.difficulty == RecipeDifficulty.MEDIUM
        assert recipe.is_vegetarian is True
        assert recipe.external_id is None
        assert recipe.external_url is None
