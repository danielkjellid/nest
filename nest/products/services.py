from decimal import Decimal
from typing import Any

import structlog
from django.core.files import File
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile
from django.http import HttpRequest
from django.utils.text import slugify

from nest.audit_logs.services import log_create_or_updated
from nest.core.exceptions import ApplicationError
from nest.core.services import model_update
from nest.data_pools.providers.oda.clients import OdaClient
from nest.data_pools.providers.oda.records import OdaProductDetailRecord
from nest.units.models import Unit
from nest.units.selectors import get_unit_by_abbreviation

from .models import Product
from .records import ProductRecord
from .selectors import _get_product, get_product

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
        fields=[
            "name",
            "gross_price",
            "gross_unit_price",
            "unit",
            "unit_quantity",
            "oda_url",
            "oda_id",
            "is_available",
            "thumbnail",
            "gtin",
            "supplier",
            "is_synced",
        ],
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


def import_from_oda(*, oda_product_id: int) -> ProductRecord | None:
    """
    Import a product from Oda based on the Oda product id.
    """

    # Get product data and image from Oda API.
    product_response = OdaClient.get_product(product_id=oda_product_id)
    product_image = OdaClient.get_image(
        url=product_response.images[0].thumbnail.url, filename="thumbnail.jpg"
    )

    def get_product_image() -> File | None:  # type: ignroe
        if not product_image:
            return None

        product_image.name = slugify(product_response.full_name)
        return product_image

    # Validate that all required values are present.
    _validate_oda_response(response_record=product_response)

    product: Product | ProductRecord

    # Some products can be excluded from the sync, if so, we want to early return.
    # The selector will throw an Application error if the product does not exit, so
    # we deliberately catch it and ignore it here.
    try:
        product = get_product(oda_id=product_response.id)

        if not getattr(product, "is_synced", True):
            return None
    except ApplicationError:
        pass

    # Get corresponding unit from product response
    unit = get_unit_by_abbreviation(
        abbreviation=product_response.unit_price_quantity_abbreviation
    )
    unit_quantity = float(product_response.gross_price) / float(
        product_response.gross_unit_price
    )

    # A set of defaults based on our own product model.
    defaults = {
        "oda_url": product_response.front_url,
        "name": product_response.full_name,
        "gross_price": product_response.gross_price,
        "gross_unit_price": product_response.gross_unit_price,
        "unit_id": unit.id,
        "unit_quantity": unit_quantity,
        "is_available": product_response.availability.is_available,
        "supplier": product_response.brand,
        "thumbnail": get_product_image(),
    }

    product_record = update_or_create_product(
        pk=None,
        oda_id=product_response.id,
        source="Oda",
        log_ignore_fields={"thumbnail"},
        **defaults,
    )

    return product_record


def _validate_oda_response(*, response_record: OdaProductDetailRecord) -> None:
    """
    Validate that required values from the Oda product response is present, and
    raise an exception if they're not.
    """
    try:
        assert response_record.id, "Oda payload did not provide an id"
        assert response_record.full_name, "Oda payload did not provide a name"
        assert response_record.gross_price, "Oda payload did not provide a gross_price"
        assert (
            response_record.unit_price_quantity_abbreviation
        ), "Oda payload did not provide a unit abbreviation"
        assert (
            response_record.availability.is_available is not None
        ), "Oda payload did not provide is_available"
    except AssertionError as exc:
        raise ApplicationError("Unable to validate Oda response") from exc
