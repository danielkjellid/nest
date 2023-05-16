from nest.core.exceptions import ApplicationError

from .models import Product
from .records import ProductRecord, ProductNutritionPrettyRecord
from .constants import PRODUCT_NUTRITION_IDENTIFIERS
from decimal import Decimal


def get_product(*, pk: int | None = None, oda_id: int | None = None) -> ProductRecord:
    """
    Get a specific product instance.
    """
    product = _get_product(pk=pk, oda_id=oda_id)
    return ProductRecord.from_product(product)


def _get_product(*, pk: int | None = None, oda_id: int | None = None) -> Product:
    """
    Get a product instance. Caution: this returns a model instance, and not a
    record, and should therefore not be used directly. Use
    get_product(...) instead.
    """
    filters = {}

    if pk is not None:
        filters["id"] = pk

    if oda_id is not None:
        filters["oda_id"] = oda_id

    product = Product.objects.filter(**filters).select_related("unit").first()

    if not product:
        raise ApplicationError(message="Product does not exist.")

    return product


def get_products() -> list[ProductRecord]:
    """
    Get a list of all products.
    """

    products = Product.objects.all().select_related("unit")
    return [ProductRecord.from_product(product) for product in products]


def get_pretty_product_nutrition(
    *, product: Product | ProductRecord
) -> list[ProductNutritionPrettyRecord]:
    accessor = product.nutrition if isinstance(product, ProductRecord) else product

    records = []
    modified_identifiers = PRODUCT_NUTRITION_IDENTIFIERS.copy()

    # energy_kj and energy_kcal are handled manually bellow.
    modified_identifiers.pop("energy_kj")
    modified_identifiers.pop("energy_kcal")

    if accessor.energy_kj is not None and accessor.energy_kcal is not None:
        records.append(
            ProductNutritionPrettyRecord(
                title="Energy",
                key="energy",
                value=(
                    f"{accessor.energy_kj.normalize()} kJ / "
                    f"{accessor.energy_kcal.normalize()} kcal"
                ),
            )
        )

    for key, fallback_value in modified_identifiers.items():
        split_key = key.split("_")
        parent_key = split_key[0]
        pretty_key = " ".join(split_key).capitalize()
        value: Decimal | None = getattr(accessor, key, fallback_value)

        if value:
            records.append(
                ProductNutritionPrettyRecord(
                    title=pretty_key,
                    value=f"{value.normalize()} g",
                    key=key,
                    parent_key=(
                        parent_key
                        if hasattr(accessor, parent_key) and parent_key != key
                        else None
                    ),
                )
            )

    return records
