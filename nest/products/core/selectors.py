from decimal import Decimal

from nest.core.exceptions import ApplicationError
from nest.core.records import TableRecord

from ..oda.constants import PRODUCT_NUTRITION_IDENTIFIERS
from .models import Product
from django.db.models import QuerySet
from .records import ProductRecord, ProductClassifiersRecord
from nest.units.records import UnitRecord
from nest.core.types import FetchedResult


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


def get_products(product_ids: list[int]) -> list[ProductRecord]:
    products = Product.objects.filter(id__in=product_ids).select_related("unit")
    records = _get_product_records_from_products(products=products)

    return records


def get_products_from_oda_ids(oda_ids: list[int]) -> list[ProductRecord]:
    products = Product.objects.filter(oda_id__in=oda_ids).select_related("unit")
    records = _get_product_records_from_products(products=products)

    return records


def _get_product_records_from_products(
    *, products: QuerySet[Product]
) -> list[ProductRecord]:
    records: list[ProductRecord] = []

    for product in products:
        unit = product.unit
        records.append(
            ProductRecord(
                id=product.id,
                name=product.name,
                full_name=product.full_name,
                gross_price=product.gross_price,
                gross_unit_price=product.gross_unit_price,
                unit=UnitRecord(
                    id=unit.id,
                    name=unit.name,
                    name_pluralized=unit.name_pluralized,
                    abbreviation=unit.abbreviation,
                    unit_type=unit.unit_type,
                    base_factor=unit.base_factor,
                    is_base_unit=unit.is_base_unit,
                    is_default=unit.is_default,
                    display_name=unit.display_name,
                ),
                unit_quantity=product.unit_quantity,
                oda_id=product.oda_id,
                oda_url=product.oda_url,
                is_available=product.is_available,
                is_synced=product.is_synced,
                last_synced_at=product.last_synced_at,
                thumbnail_url=product.thumbnail.url if product.thumbnail else None,
                gtin=product.gtin,
                supplier=product.supplier,
                is_oda_product=product.is_oda_product,
                last_data_update=product.last_data_update,
                display_price=product.display_price,
                ingredients=product.ingredients,
                allergens=product.allergens,
                classifiers=ProductClassifiersRecord(
                    contains_lactose=product.contains_lactose,
                    contains_gluten=product.contains_gluten,
                ),
                energy_kj=product.energy_kj,
                energy_kcal=product.energy_kcal,
                fat=product.fat,
                fat_saturated=product.fat_saturated,
                fat_monounsaturated=product.fat_monounsaturated,
                fat_polyunsaturated=product.fat_polyunsaturated,
                carbohydrates=product.carbohydrates,
                carbohydrates_sugars=product.carbohydrates_sugars,
                carbohydrates_polyols=product.carbohydrates_polyols,
                carbohydrates_starch=product.carbohydrates_starch,
                fibres=product.fibres,
                protein=product.protein,
                salt=product.salt,
                sodium=product.sodium,
            )
        )

    return records


def get_product2(*, pk: int | None = None, oda_id: int | None = None):
    # TODO: raise error if no parameter is raised

    filters = {}

    if pk is not None:
        filters["id"] = pk

    if oda_id is not None:
        filters["oda_id"] = oda_id

    product = Product.objects.filter(**filters).select_related("unit").first()

    if not product:
        raise ApplicationError(message="Product does not exist.")

    unit = product.unit
    return ProductRecord(
        id=product.id,
        name=product.name,
        full_name=product.full_name,
        gross_price=product.gross_price,
        gross_unit_price=product.gross_unit_price,
        unit=UnitRecord(
            id=unit.id,
            name=unit.name,
            name_pluralized=unit.name_pluralized,
            abbreviation=unit.abbreviation,
            unit_type=unit.unit_type,
            base_factor=unit.base_factor,
            is_base_unit=unit.is_base_unit,
            is_default=unit.is_default,
            display_name=unit.display_name,
        ),
        unit_quantity=product.unit_quantity,
        oda_id=product.oda_id,
        oda_url=product.oda_url,
        is_available=product.is_available,
        is_synced=product.is_synced,
        last_synced_at=product.last_synced_at,
        thumbnail_url=product.thumbnail.url if product.thumbnail else None,
        gtin=product.gtin,
        supplier=product.supplier,
    )


def get_products() -> list[ProductRecord]:
    """
    Get a list of all products.
    """

    products = Product.objects.all().select_related("unit")
    return [ProductRecord.from_product(product) for product in products]


def get_nutrition_table(*, product: Product | ProductRecord) -> list[TableRecord]:
    records = []
    modified_identifiers = PRODUCT_NUTRITION_IDENTIFIERS.copy()

    # energy_kj and energy_kcal are handled manually bellow.
    modified_identifiers.pop("energy_kj")
    modified_identifiers.pop("energy_kcal")

    if product.energy_kj is not None and product.energy_kcal is not None:
        records.append(
            TableRecord(
                title="Energy",
                key="energy",
                value=(
                    f"{product.energy_kj.normalize()} kJ / "  # type: ignore
                    f"{product.energy_kcal.normalize()} kcal"  # type: ignore
                ),
            )
        )

    for key, fallback_value in modified_identifiers.items():
        split_key = key.split("_")
        parent_key = split_key[0]
        pretty_key = " ".join(split_key).capitalize()
        value: Decimal | None = getattr(product, key, fallback_value)

        if value:
            records.append(
                TableRecord(
                    title=pretty_key,
                    value=f"{value.normalize()} g",
                    key=key,
                    parent_key=(
                        parent_key
                        if hasattr(product, parent_key) and parent_key != key
                        else None
                    ),
                )
            )

    return records
