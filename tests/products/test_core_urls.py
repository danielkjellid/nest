import pytest
from django.urls import reverse

urls = [
    ("product_list_api", "/api/v1/products/", None),
    ("product_create_api", "/api/v1/products/create/", None),
    ("product_detail_api", "/api/v1/products/product_id/", ["product_id"]),
    ("product_edit_api", "/api/v1/products/product_id/edit/", ["product_id"]),
]


@pytest.mark.parametrize("url_name, url, args", urls)
def test_products_core_urls(
    url_name: str, url: str, args: list[str | int] | None
) -> None:
    """
    Test reverse matches for endpoints.
    """

    reversed_url = reverse(f"api-1.0.0:{url_name}", args=args)
    assert reversed_url == url
