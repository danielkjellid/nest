from decimal import Decimal
from typing import Any

import structlog
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile
from django.http import HttpRequest

from nest.audit_logs.services import log_create_or_updated
from nest.core.services import model_update
from nest.units.models import Unit

from .models import Product
from .records import ProductRecord
from .selectors import _get_product

logger = structlog.getLogger()


def create_product(
    *,
    name: str,
    gross_price: str,
    unit_id: int | str,
    unit_quantity: str,
    supplier: str,
    thumbnail: UploadedFile | InMemoryUploadedFile | ImageFile | None = None,
    request: HttpRequest | None = None,
    **additional_fields: Any,
) -> ProductRecord:
    """
    Create a single product instance.
    """

    additional_fields.pop("gross_unit_price", None)
    gross_unit_price = Decimal(gross_price) / Decimal(unit_quantity)

    product = Product(
        name=name,
        gross_price=Decimal(gross_price),
        unit_id=unit_id,
        unit_quantity=Decimal(unit_quantity),
        supplier=supplier,
        gross_unit_price=gross_unit_price.normalize(),
        **additional_fields,
    )

    if thumbnail is not None:
        product.thumbnail = thumbnail

    product.full_clean()
    product.save()

    log_create_or_updated(old=None, new=product, request_or_user=request)
    return ProductRecord.from_product(product)


def edit_product(
    *,
    request: HttpRequest | None = None,
    product_id: int,
    thumbnail: UploadedFile | InMemoryUploadedFile | ImageFile | None = None,
    **edits: Any,
) -> ProductRecord:
    """
    Edit an existing product instance.
    """

    data = edits.copy()

    if thumbnail is not None:
        data["thumbnail"] = thumbnail

    if "unit_id" in data:
        unit = Unit.objects.get(id=data.pop("unit_id"))
        data["unit"] = unit

    product_instance, _has_updated = model_update(
        instance=_get_product(pk=product_id),
        data=data,
        request=request,
        log_ignore_fields={"thumbnail"},
    )

    return ProductRecord.from_product(product_instance)


def update_or_create_product(
    *,
    pk: int | None = None,
    oda_id: int | None = None,
    source: str | None = None,
    log_ignore_fields: set[str] | None = None,
    **kwargs: Any,
) -> ProductRecord:
    """
    Update or create a product.
    """
    filters: dict[str, int | None] = {}
    defaults = kwargs.copy()

    if pk is not None:
        filters["id"] = pk
    elif oda_id is not None:
        filters["oda_id"] = oda_id
        defaults["oda_id"] = oda_id
    else:
        # Filters need to be explicitly set to None, so we won't find any existing
        # products.
        filters = {"id": pk, "oda_id": oda_id}

    existing_product = Product.objects.filter(**filters).select_related(
        "unit", "ingredient"
    )

    if existing_product:
        assert (
            len(existing_product) == 1
        ), "Found multiple products with filters, cannot safely update."

        existing_product.update(**defaults)
        updated_product = existing_product.first()
        product = updated_product
    else:
        product = Product.objects.create(**defaults)

    assert product

    log_create_or_updated(
        old=existing_product.first(),
        new=product,
        source=source,
        ignore_fields=log_ignore_fields,
    )

    return ProductRecord.from_product(product)
