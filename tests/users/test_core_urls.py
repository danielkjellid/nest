from django.urls import reverse
import pytest

urls = [("user_list_api", "/api/v1/users/", None)]


@pytest.mark.parametrize("url_name, url, args", urls)
def test_users_core_urls(url_name: str, url: str, args: list[str | int] | None) -> None:
    """
    Test reverse matches for endpoints.
    """

    reversed_url = reverse(f"api-1.0.0:{url_name}", args=args)
    assert reversed_url == url
