from typing import Any

from django.http import HttpRequest
from ninja import File, Form, Router, Schema
from store_kit.http import status

from nest.api.files import UploadedFile
from nest.api.responses import APIResponse
from nest.audit_logs.selectors import get_log_entries_for_object
from nest.core.decorators import staff_required
from nest.core.records import TableRecord
from nest.core.utils import format_datetime

from .forms import ProductCreateForm, ProductEditForm
from .models import Product
from .selectors import get_nutrition_table, get_product, get_products
from .services import create_product, edit_product

router = Router(tags=["Products"])


class ProductListOut(Schema):
    id: int
    full_name: str
    thumbnail_url: str | None
    is_available: bool
    oda_url: str | None
    oda_id: int | None
    is_synced: bool
    gtin: str | None
    is_oda_product: bool
    display_price: str


@router.get("/", response=APIResponse[list[ProductListOut]])
def product_list_api(request: HttpRequest) -> APIResponse[list[ProductListOut]]:
    """
    Get a list of all products in the application.
    """
    products = get_products()
    data = [ProductListOut(**product.dict()) for product in products]

    return APIResponse(status="success", data=data)


@router.post("create/", response={201: APIResponse[None]})
@staff_required
def product_create_api(
    request: HttpRequest,
    payload: ProductCreateForm = Form(...),  # noqa
    thumbnail: UploadedFile | None = File(None),  # noqa
) -> tuple[int, APIResponse[None]]:
    """
    Create a normal product.
    """

    create_product(**payload.dict(), thumbnail=thumbnail, request=request)
    return status.HTTP_201_CREATED, APIResponse(status="success", data=None)


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
    display_name: str | None


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

    fat: str | None
    fat_saturated: str | None
    fat_monounsaturated: str | None
    fat_polyunsaturated: str | None
    carbohydrates: str | None
    carbohydrates_sugars: str | None
    carbohydrates_polyols: str | None
    carbohydrates_starch: str | None
    fibres: str | None
    salt: str | None
    sodium: str | None

    nutrition_table: list[TableRecord]

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
    nutrition_table = get_nutrition_table(product=product)

    product_dict = product.dict()
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
            nutrition_table=nutrition_table,
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


@router.post("{product_id}/edit/", response=APIResponse[None])
@staff_required
def product_edit_api(
    request: HttpRequest,
    product_id: int,
    payload: ProductEditForm = Form(...),  # noqa
    thumbnail: UploadedFile | None = File(None),  # noqa
) -> APIResponse[None]:
    """
    Edit a product.
    """
    edit_product(
        request=request, product_id=product_id, thumbnail=thumbnail, **payload.dict()
    )
    return APIResponse(status="success", data=None)
