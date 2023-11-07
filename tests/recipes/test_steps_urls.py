import pytest
from django.urls import reverse

urls = [
    (
        "recipe_steps_create_api",
        "/api/v1/recipes/steps/recipe_id/create/",
        ["recipe_id"],
    ),
]


@pytest.mark.parametrize("url_name, url, args", urls)
def test_recipes_steps_urls(
    url_name: str, url: str, args: list[str | int] | None
) -> None:
    """
    Test reverse matches for endpoints.
    """

    reversed_url = reverse(f"api-1.0.0:{url_name}", args=args)
    assert reversed_url == url
