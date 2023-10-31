from decimal import Decimal
from typing import Any

from django.http import HttpRequest
from ninja import File, Form, Router, Schema

from nest.api.fields import FormField
from nest.api.files import UploadedFile
from nest.api.responses import APIResponse
from nest.audit_logs.selectors import get_log_entries_for_object
from nest.core.decorators import staff_required
from nest.core.records import TableRecord
from nest.core.utils import format_datetime
from nest.frontend.components import FrontendComponents

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


class ProductCreateIn(Schema):
    name: str = FormField(
        ...,
        order=1,
        help_text="Plain name of product, should not include unit.",
    )
    gross_price: str = FormField(
        ..., order=2, help_text="Gross price of product, including VAT."
    )
    unit_quantity: str = FormField(
        ...,
        order=3,
        help_text="Amount in selected unit type. E.g. 2 if 2 kg.",
        col_span=1,
    )
    unit_id: int = FormField(
        ...,
        alias="unit",
        help_text="What sort of unit is this?",
        col_span=1,
        order=4,
        component=FrontendComponents.SELECT.value,
    )
    supplier: str = FormField(..., order=5)
    gtin: str | None = FormField(None, order=6)
    ingredients: str | None = FormField(
        None,
        order=7,
        help_text="Specify ingredients seperated by a comma. E.g. milk, egg, sugar.",
        component=FrontendComponents.TEXT_AREA.value,
    )
    allergens: str | None = FormField(
        None,
        order=8,
        help_text="Specify allergens seperated by a comma. E.g. milk, egg, sugar.",
        component=FrontendComponents.TEXT_AREA.value,
    )
    fat: str | None = FormField(None, order=9, col_span=1)
    fat_saturated: str | None = FormField(None, order=10, col_span=1)
    fat_monounsaturated: str | None = FormField(None, order=11, col_span=1)
    fat_polyunsaturated: str | None = FormField(None, order=12, col_span=1)
    carbohydrates: str | None = FormField(None, order=13, col_span=1)
    carbohydrates_sugars: str | None = FormField(None, order=14, col_span=1)
    carbohydrates_polyols: str | None = FormField(None, order=15, col_span=1)
    carbohydrates_starch: str | None = FormField(None, order=16, col_span=1)
    fibres: str | None = FormField(None, order=17, col_span=2)
    salt: str | None = FormField(None, order=18, col_span=2)
    sodium: str | None = FormField(None, order=19, col_span=2)
    is_available: bool = FormField(..., order=20, default_value=True)

    class FormMeta:
        columns = 2


@router.post("create/", response=APIResponse[None])
@staff_required
def product_create_api(
    request: HttpRequest,
    payload: ProductCreateIn = Form(...),  # noqa
    thumbnail: UploadedFile | None = File(None),  # noqa
) -> APIResponse[None]:
    """
    Create a normal product.
    """

    create_product(**payload.dict(), thumbnail=thumbnail, request=request)
    return APIResponse(status="success", data=None)


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


class ProductEditIn(Schema):
    name: str = FormField(
        ...,
        order=1,
        help_text="Plain name of product, should not include unit.",
    )
    gross_price: Decimal = FormField(
        ..., order=2, help_text="Gross price of product, including VAT."
    )
    unit_quantity: Decimal = FormField(
        ...,
        order=3,
        help_text="Amount in selected unit type. E.g. 2 if 2 kg.",
        col_span=2,
    )
    unit_id: int = FormField(
        ...,
        alias="unit",
        order=4,
        help_text="What sort of unit is this?",
        col_span=2,
        component=FrontendComponents.SELECT.value,
    )
    supplier: str = FormField(..., order=5)
    gtin: str | None = FormField(
        None,
        order=6,
        help_text="Global trade item number. Number bellow barcode.",
    )
    oda_id: int | None = FormField(
        None, order=7, help_text="Corresponding product id at Oda."
    )
    oda_url: str | None = FormField(None, order=8, help_text="Link to product at Oda.")
    fat: str | None = FormField(None, order=9, col_span=1)
    fat_saturated: str | None = FormField(None, order=10, col_span=1)
    fat_monounsaturated: str | None = FormField(None, order=11, col_span=1)
    fat_polyunsaturated: str | None = FormField(None, order=12, col_span=1)
    carbohydrates: str | None = FormField(None, order=13, col_span=1)
    carbohydrates_sugars: str | None = FormField(None, order=14, col_span=1)
    carbohydrates_polyols: str | None = FormField(None, order=15, col_span=1)
    carbohydrates_starch: str | None = FormField(None, order=16, col_span=1)
    fibres: str | None = FormField(None, order=17, col_span=4)
    salt: str | None = FormField(None, order=18, col_span=4)
    sodium: str | None = FormField(None, order=19, col_span=4)
    is_available: bool = FormField(
        ...,
        order=20,
        help_text="Product is available and is actively used in recipes.",
    )
    is_synced: bool = FormField(
        ...,
        order=21,
        help_text="Product is synced with external providers",
    )

    class FormMeta:
        columns = 4


@router.post("{product_id}/edit/", response=APIResponse[None])
@staff_required
def product_edit_api(
    request: HttpRequest,
    product_id: int,
    payload: ProductEditIn = Form(...),  # noqa
    thumbnail: UploadedFile | None = File(None),  # noqa
) -> APIResponse[None]:
    """
    Edit a product.
    """
    edit_product(
        request=request, product_id=product_id, thumbnail=thumbnail, **payload.dict()
    )
    return APIResponse(status="success", data=None)
