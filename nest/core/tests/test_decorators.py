import pytest

from nest.products.models import Product
from nest.products.tests.utils import create_product

from ..decorators import ensure_prefetched_relations

pytestmark = pytest.mark.django_db


def test_decorator_ensure_prefetched_relations():
    """
    Test that the ensure_prefetched_relations decorator raises errors when fields are
    not prefetched or intentionally skipped.
    """
    product = create_product()
    product_with_relations = (
        Product.objects.select_related("unit", "ingredient")
        .filter(id=product.id)
        .first()
    )
    product_with_relation_unit_skipped = (
        Product.objects.select_related("ingredient").filter(id=product.id).first()
    )

    @ensure_prefetched_relations(arg_or_kwarg="product")
    def dummy_arg_func(product: Product):
        ...

    @ensure_prefetched_relations(arg_or_kwarg="product")
    def dummy_kwarg_func(*, product: Product):
        ...

    @ensure_prefetched_relations(arg_or_kwarg="product", skip_fields=["unit"])
    def dummy_func_skip_fields(product: Product):
        ...

    # Test that RuntimeError is raised if product does not have any select/prefetch
    # related.
    with pytest.raises(RuntimeError):
        dummy_arg_func(product)
        dummy_kwarg_func(product=product)

    # Test that RuntimeError is raised when there are no arguments that match the passed
    # arg_or_kwarg
    with pytest.raises(RuntimeError):
        dummy_arg_func("should-not-pass")

    dummy_arg_func(product_with_relations)
    dummy_kwarg_func(product=product_with_relations)
    dummy_func_skip_fields(product=product_with_relation_unit_skipped)
