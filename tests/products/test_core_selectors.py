import pytest


@pytest.mark.products(
    {
        "product1": {"name": "Product 1"},
        "product2": {"name": "Product 2"},
        "product3": {"name": "Product 3"},
    }
)
def test_selector_get_products(products) -> None:
    ...
