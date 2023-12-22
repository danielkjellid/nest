from django.http import HttpRequest
from ninja import File, Form, Router
from store_kit.http import status

from nest.api.files import UploadedFile
from nest.api.responses import APIResponse
from nest.core.decorators import staff_required
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


@router.get("{product_id}/", response=APIResponse[ProductRecord])
def product_detail_api(
    request: HttpRequest, product_id: int
) -> APIResponse[ProductRecord]:
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
