from typing import Any

from django.http import HttpRequest
from ninja import File, Form, Router, Schema
from store_kit.http import status

from nest.api.files import UploadedFile
from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
from nest.core.records import TableRecord
from nest.core.utils import Exclude

from .forms import ProductCreateForm, ProductEditForm
from .records import ProductRecord
from .selectors import get_product, get_products
from .services import create_product, edit_product

router = Router(tags=["Products"])


@router.get("/", response=APIResponse[list[ProductRecord]])
def product_list_api(request: HttpRequest) -> APIResponse[list[ProductRecord]]:
    """
    Get a list of all products in the application.
    """
    products = get_products()
    return APIResponse(status="success", data=products)


ProductCreateIn = Exclude("ProductCreateIn", ProductCreateForm, ["thumbnail"])


@router.post("create/", response={201: APIResponse[None]})
@staff_required
def product_create_api(
    request: HttpRequest,
    payload: ProductCreateIn = Form(...),  # type: ignore # noqa
    thumbnail: UploadedFile | None = File(None),  # noqa
) -> tuple[int, APIResponse[None]]:
    """
    Create a normal product.
    """

    create_product(
        **payload.dict(),  # type: ignore
        thumbnail=thumbnail,
        request=request,
    )
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
    return APIResponse(status="success", data=product)


ProductEditIn = Exclude("ProductEditIn", ProductEditForm, ["thumbnail"])


@router.post("{product_id}/edit/", response=APIResponse[None])
@staff_required
def product_edit_api(
    request: HttpRequest,
    product_id: int,
    payload: ProductEditIn = Form(...),  # type: ignore # noqa
    thumbnail: UploadedFile | None = File(None),  # noqa
) -> APIResponse[None]:
    """
    Edit a product.
    """
    edit_product(
        request=request,
        product_id=product_id,
        thumbnail=thumbnail,
        **payload.dict(),  # type: ignore
    )
    return APIResponse(status="success", data=None)
