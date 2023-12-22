import pytest
from unittest.mock import MagicMock
from nest.products.core.models import Product
from nest.products.core.selectors import get_products
from typing import Any


@pytest.mark.products(
    product1={"name": "Product 1"},
    product2={"name": "Product 2"},
    product3={"name": "Product 3"},
)
@pytest.mark.oda_product(name="Oda product")
def test_selector_get_products(
    oda_product: Product,
    products: dict[str, Product],
    mocker: MagicMock,
    django_assert_num_queries: Any,
) -> None:
    log_entries_mock_return = {
        oda_product.id: [],
        **{p.id: [] for p in products.values()},
    }

    print(log_entries_mock_return)
    log_entries_mock = mocker.patch(
        "nest.products.core.selectors.get_log_entries_for_objects",
        return_value=log_entries_mock_return,
    )

    normal_product_ids = [p.id for p in products.values()]
    oda_product_ids = [oda_product.id]

    with django_assert_num_queries(1):
        all_products = get_products()

    assert set(p.id for p in all_products) == set(normal_product_ids + oda_product_ids)
    log_entries_mock.assert_called_once_with(
        model=Product,
        ids=oda_product_ids + normal_product_ids,
        limit=10,
    )
    log_entries_mock.reset_mock()

    with django_assert_num_queries(1):
        normal_products = get_products(product_ids=normal_product_ids)

    assert set(p.id for p in normal_products) == set(normal_product_ids)
    log_entries_mock.assert_called_once_with(
        model=Product,
        ids=normal_product_ids,
        limit=10,
    )
    log_entries_mock.reset_mock()

    with django_assert_num_queries(1):
        oda_products = get_products(oda_ids=[oda_product.oda_id])

    assert set(p.id for p in oda_products) == set(oda_product_ids)
    log_entries_mock.assert_called_once_with(
        model=Product,
        ids=oda_product_ids,
        limit=10,
    )
