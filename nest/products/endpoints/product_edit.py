from django.http import HttpRequest
from ninja import File, Form, Schema

from nest.api.files import UploadedFile
from nest.api.responses import APIResponse
from nest.core.decorators import staff_required

from .router import router


class ProductEditIn(Schema):
    id: str

    class FormMeta:
        columns = 2


@router.put("{product_id}/edit/", response=APIResponse[None])
@staff_required
def product_edit_api(
    request: HttpRequest,
    product_id: int,
    payload: ProductEditIn = Form(...),
    thumbnail: UploadedFile | None = File(None),
) -> APIResponse[None]:
    """
    Edit a product.
    """

    return APIResponse(status="success", data=None)
