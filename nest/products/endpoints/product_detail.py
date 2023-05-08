from django.http import HttpRequest
from ninja import Schema

from nest.api.responses import APIResponse
from nest.products.selectors import get_product
from typing import Any
from .router import router
from nest.products.models import Product
from nest.audit_logs.selectors import get_log_entries_for_object
from nest.core.utils import format_datetime


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


class ProductDetailOut(Schema):
    id: int
    name: str
    full_name: str
    gross_price: str
    gross_unit_price: str | None
    unit: ProductDetailUnitOut
    unit_quantity: str | None
    oda_url: str | None
    oda_id: str | None
    is_available: bool
    thumbnail_url: str | None
    gtin: str | None
    supplier: str
    is_synced: bool
    is_oda_product: bool
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

    return APIResponse(
        status="success",
        data=ProductDetailOut(
            **product.dict(),
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
