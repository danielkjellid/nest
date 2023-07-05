from typing import Any

from django.http import HttpRequest
from ninja import Schema

from nest.api.responses import APIResponse
from nest.audit_logs.selectors import get_log_entries_for_object
from nest.core.utils import format_datetime
from nest.products.models import Product
from nest.products.selectors import get_product, get_pretty_product_nutrition

from .router import router


class ProductDetailAuditLogsOut(Schema):
    user_or_source: str | None
    remote_addr: str | None
    changes: dict[str, tuple[Any | None, Any | None]]
    created_at: str


class ProductDetailUnitOut(Schema):
    id: int
    name: str
    abbreviation: str
    unit_type: str
    display_name: str


class ProductDetailNutritionOut(Schema):
    key: str
    parent_key: str | None
    title: str
    value: str


class ProductDetailOut(Schema):
    id: int
    name: str
    full_name: str
    is_available: bool
    thumbnail_url: str | None

    contains_lactose: bool = False
    contains_gluten: bool = False

    gross_price: str
    gross_unit_price: str | None

    unit: ProductDetailUnitOut
    unit_quantity: str | None

    gtin: str | None
    supplier: str | None

    is_synced: bool
    oda_id: str | None
    oda_url: str | None
    is_oda_product: bool
    last_data_update: str | None

    nutrition: list[ProductDetailNutritionOut]

    audit_logs: list[ProductDetailAuditLogsOut]


@router.get("{product_id}/", response=APIResponse[ProductDetailOut])
def product_detail_api(
    request: HttpRequest, product_id: int
) -> APIResponse[ProductDetailOut]:
    """
    Retrieve a single product instance based on product id.
    """
    product = get_product(pk=product_id)
    product_log_entries = get_log_entries_for_object(model=Product, pk=product_id)
    nutrition = get_pretty_product_nutrition(product=product)

    product_dict = product.dict()
    product_dict.pop("nutrition")
    last_data_update = product_dict.pop("last_data_update", None)

    return APIResponse(
        status="success",
        data=ProductDetailOut(
            **product_dict,
            last_data_update=(
                format_datetime(last_data_update, with_seconds=True)
                if last_data_update
                else None
            ),
            nutrition=nutrition,
            audit_logs=[
                ProductDetailAuditLogsOut(
                    user_or_source=log_entry.source
                    if log_entry.source
                    else log_entry.user.full_name
                    if log_entry.user
                    else None,
                    remote_addr=log_entry.remote_addr,
                    changes=log_entry.changes,
                    created_at=format_datetime(log_entry.created_at),
                )
                for log_entry in product_log_entries[:10]
            ],  # Only show last 10 entries.
        ),
    )
