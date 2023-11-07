from django.urls import reverse
import pytest

urls = [
    ("recipe_ingredient_create_api", "/api/v1/recipes/ingredients/create/", None),
    ("recipe_ingredient_delete_api", "/api/v1/recipes/ingredients/delete/", None),
    ("recipe_ingredient_list_api", "/api/v1/recipes/ingredients/", None),
    (
        "recipe_ingredient_groups_create_api",
        "/api/v1/recipes/ingredients/recipe_id/groups/create/",
        ["recipe_id"],
    ),
    (
        "recipe_ingredient_groups_list_api",
        "/api/v1/recipes/ingredients/recipe_id/groups/",
        ["recipe_id"],
    ),
]


@pytest.mark.parametrize("url_name, url, args", urls)
def test_recipes_ingredients_urls(
    url_name: str, url: str, args: list[str | int] | None
) -> None:
    """
    Test reverse matches for endpoints.
    """

    reversed_url = reverse(f"api-1.0.0:{url_name}", args=args)
    assert reversed_url == url
