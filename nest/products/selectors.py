from django.db.models import Q

from nest.core.exceptions import ApplicationError
from .models import Product
from .records import ProductRecord


class ProductSelector:
    def __init__(self) -> None:
        ...

    @classmethod
    def get_product(
        cls, pk: int | None = None, oda_id: int | None = None
    ) -> ProductRecord:
        """
        Get a specific product instance.
        """
        product = cls._get_product(pk=pk, oda_id=oda_id)
        return ProductRecord.from_product(product)

    @classmethod
    def all_products(cls) -> list[ProductRecord]:
        """
        Get a list of all products.
        """

        products = Product.objects.all().select_related("unit")
        return [ProductRecord.from_product(product) for product in products]

    @classmethod
    def _get_product(cls, pk: int | None = None, oda_id: int | None = None) -> Product:
        """
        Get a product instance. Caution: this returns a model instance, and not a
        record, and should therefore not be used directly. Use
        ProductSelector.get_product(...) instead.
        """
        product = (
            Product.objects.filter(Q(id=pk) | Q(oda_id=oda_id))
            .select_related("unit")
            .first()
        )

        if not product:
            raise ApplicationError(message="Product does not exist.")

        return product
