import pytest

from nest.core.exceptions import ApplicationError
from nest.products.records import ProductRecord
from nest.products.selectors import (
    _get_product,
    get_product,
    get_products,
)
from nest.products.tests.utils import create_product

pytestmark = pytest.mark.django_db


class TestProductsSelectors:
    def test_get_product(self, django_assert_num_queries, mocker):
        """
        Test that the get_product selector correctly calls the _get_product selector
        that performs the query itself.
        """
        product = create_product()
        _get_product_selector_mock = mocker.patch(
            f"{_get_product.__module__}.{_get_product.__name__}", return_value=product
        )
        gotten_product = get_product(pk=product.id)

        call_args = _get_product_selector_mock.call_args.kwargs
        assert _get_product_selector_mock.call_count == 1
        assert call_args["pk"] == product.pk
        assert gotten_product == ProductRecord.from_product(product)

    def test_all_products(self, django_assert_num_queries):
        """
        Test that the all_products selector returns expected output within
        query limits.
        """
        create_product(name="Test product 1")
        create_product(name="Test product 2")
        create_product(name="Test product 3")

        with django_assert_num_queries(1):
            products = get_products()

        assert len(products) == 3

    def test__get_product(self, django_assert_num_queries):
        """
        Test that the _get_product selector returns expected product within
        query limits.
        """
        product1 = create_product()
        product2 = create_product(oda_id=1111)

        # Test that the correct product is retrieved by passing pk.
        with django_assert_num_queries(1):
            product_by_pk = _get_product(pk=product1.id)

        assert product_by_pk.id == product1.id

        # Test that the correct product is retrieved by passing oda_id.
        with django_assert_num_queries(1):
            product_by_oda_id = _get_product(oda_id=product2.oda_id)

        assert product_by_oda_id.id == product2.id

        # Test that ApplicationError is raised when product is None.
        with pytest.raises(ApplicationError):
            _get_product(pk=999)
