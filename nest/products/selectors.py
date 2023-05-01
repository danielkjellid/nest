from django.db.models import Q

from nest.core.exceptions import ApplicationError

from .models import Product
from .records import ProductRecord


def get_product(pk: int | None = None, oda_id: int | None = None) -> ProductRecord:
    """
    Get a specific product instance.
    """
    product = _get_product(pk=pk, oda_id=oda_id)
    return ProductRecord.from_product(product)


def _get_product(pk: int | None = None, oda_id: int | None = None) -> Product:
    """
    Get a product instance. Caution: this returns a model instance, and not a
    record, and should therefore not be used directly. Use
    get_product(...) instead.
    """
    product = (
        Product.objects.filter(Q(id=pk) | Q(oda_id=oda_id))
        .select_related("unit")
        .first()
    )

    if not product:
        raise ApplicationError(message="Product does not exist.")

    return product


def get_products() -> list[ProductRecord]:
    """
    Get a list of all products.
    """

    products = Product.objects.all().select_related("unit")
    return [ProductRecord.from_product(product) for product in products]
