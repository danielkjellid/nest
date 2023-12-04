from nest.recipes.core.enums import RecipeDifficulty, RecipeStatus
from nest.recipes.core.models import Recipe
from nest.recipes.core.services import create_recipe


def test_service_create_recipe(django_assert_num_queries):
    """
    Test that the create_recipe service successfully creates a recipe with expected
    output.
    """

    initial_count = Recipe.objects.count()

    fields = {
        "title": "A new recipe",
        "default_num_portions": 3,
        "status": "draft",
        "difficulty": "medium",
        "is_vegetarian": True,
    }

    with django_assert_num_queries(3):
        recipe = create_recipe(**fields)

    assert Recipe.objects.count() == initial_count + 1

    assert recipe.title == fields["title"]
    assert recipe.default_num_portions == fields["default_num_portions"]
    assert recipe.status == RecipeStatus.DRAFT
    assert recipe.difficulty == RecipeDifficulty.MEDIUM
    assert recipe.is_vegetarian is True
    assert recipe.external_id is None
    assert recipe.external_url is None
