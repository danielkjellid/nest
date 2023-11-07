import pytest
from django.urls import reverse

urls = [
    ("product_oda_import_api", "/api/v1/products/oda/import/", None),
    (
        "product_oda_import_confirm_api",
        "/api/v1/products/oda/import/confirm/",
        None,
    ),
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
