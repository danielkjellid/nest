from decimal import Decimal
from typing import Any

import structlog
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile
from django.http import HttpRequest

from nest.audit_logs.services import log_create_or_updated
from nest.core.services import model_update
from nest.units.models import Unit

from ..models import Product
from ..records import ProductRecord
from ..selectors import _get_product

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

    if pk is None and oda_id is not None:
        existing_product = Product.objects.filter(oda_id=oda_id).first()
        product, created = Product.objects.update_or_create(
            oda_id=oda_id,
            defaults=kwargs,
        )

        log_create_or_updated(old=existing_product, new=product, source=source)
    elif pk is not None:
        defaults = kwargs

        if oda_id is not None:
            defaults.update({"oda_id": oda_id})

        existing_product = Product.objects.filter(id=pk).first()
        product, created = Product.objects.update_or_create(
            id=pk,
            defaults=defaults,
        )

        log_create_or_updated(
            old=existing_product,
            new=product,
            source=source,
            ignore_fields=log_ignore_fields,
        )
    else:
        raise ValueError("Either pk or oda_id (or both) must be passed.")

    return ProductRecord.from_product(product)
