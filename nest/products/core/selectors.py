from decimal import Decimal

from nest.audit_logs.selectors import get_log_entries_for_objects
from nest.core.exceptions import ApplicationError
from nest.core.records import TableRecord
from nest.core.utils import format_datetime
from nest.units.enums import UnitType
from nest.units.records import UnitRecord

from ..oda.constants import PRODUCT_NUTRITION_IDENTIFIERS
from .models import Product
from .records import ProductClassifiersRecord, ProductRecord


def get_product(*, pk: int) -> ProductRecord:
    try:
        products = get_products(product_ids=[pk])
        return products[0]
    except IndexError as exc:
        raise ApplicationError(message="Product does not exist.") from exc


def get_oda_product(*, oda_id: int) -> ProductRecord:
    try:
        products = get_products(oda_ids=[oda_id])
        return products[0]
    except IndexError as exc:
        raise ApplicationError(message="Oda product does not exist.") from exc


def get_products(
    *, product_ids: list[int] | None = None, oda_ids: list[int] | None = None
) -> list[ProductRecord]:
    """
    Get a list of all products.
    """

    filters = {}
    if product_ids:
        filters["id__in"] = product_ids

    if oda_ids:
        filters["oda_id__in"] = oda_ids

    products = Product.objects.filter(**filters).select_related("unit").distinct("id")
    ids = [product.id for product in products]

    log_entries = get_log_entries_for_objects(model=Product, ids=ids, limit=10)

    return [
        ProductRecord(
            id=product.id,
            name=product.name,
            full_name=product.full_name,
            gross_price=product.gross_price,
            gross_unit_price=product.gross_unit_price,
            unit=UnitRecord(
                id=product.unit.id,
                name=product.unit.name,
                name_pluralized=product.unit.name_pluralized,
                abbreviation=product.unit.abbreviation,
                unit_type=UnitType(product.unit.unit_type),
                base_factor=product.unit.base_factor,
                is_base_unit=product.unit.is_base_unit,
                is_default=product.unit.is_default,
                display_name=getattr(product.unit, "display_name", None),
            ),
            unit_quantity=product.unit_quantity,
            oda_url=product.oda_url,
            oda_id=product.oda_id,
            is_available=product.is_available,
            is_synced=product.is_synced,
            last_synced_at=product.last_synced_at,
            thumbnail_url=product.thumbnail.url if product.thumbnail else None,
            gtin=product.gtin,
            supplier=product.supplier,
            is_oda_product=product.is_oda_product,
            last_data_update=product.last_data_update,
            last_data_update_display=(
                format_datetime(product.last_data_update, with_seconds=True)
                if product.last_data_update
                else None
            ),
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
            nutrition_table=get_nutrition_table(product=product),
            audit_logs=log_entries[product.id],
        )
        for product in products
    ]


def get_nutrition_table(*, product: Product) -> list[TableRecord]:
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
