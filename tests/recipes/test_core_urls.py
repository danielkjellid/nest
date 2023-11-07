import pytest
from django.urls import reverse

urls = [
    ("recipe_create_api", "/api/v1/recipes/create/", None),
    ("recipe_detail_api", "/api/v1/recipes/recipe/recipe_id/", ["recipe_id"]),
    ("recipe_list_api", "/api/v1/recipes/", None),
]


@pytest.mark.parametrize("url_name, url, args", urls)
def test_recipes_core_urls(
    url_name: str, url: str, args: list[str | int] | None
) -> None:
    """
    Test reverse matches for endpoints.
    """

    reversed_url = reverse(f"api-1.0.0:{url_name}", args=args)
    assert reversed_url == url
