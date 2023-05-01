from decimal import Decimal
from typing import Any

import structlog
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile

from nest.core.exceptions import ApplicationError
from nest.data_pools.providers.oda.clients import OdaClient
from nest.data_pools.providers.oda.records import OdaProductDetailRecord
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

    return ProductRecord.from_product(product)


def update_or_create_product(
    *, pk: int | None = None, oda_id: int | None = None, **kwargs: Any
) -> ProductRecord:
    """
    Update or create a product.
    """

    if pk is None and oda_id is not None:
        product, _created = Product.objects.update_or_create(
            oda_id=oda_id,
            defaults=kwargs,
        )
    else:
        defaults = kwargs

        if oda_id is not None:
            defaults.update({"oda_id": oda_id})

        product, _created = Product.objects.update_or_create(
            id=pk,
            defaults=defaults,
        )

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
    }

    product_record = update_or_create_product(
        pk=None, oda_id=product_response.id, **defaults
    )

    if product_image:
        product = _get_product(pk=product_record.id)
        product.thumbnail.save("thumbnail.jpg", product_image)

        return ProductRecord.from_product(product)

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
        assert response_record.brand, "Oda payload did not provide a supplier"
        assert (
            response_record.availability.is_available is not None
        ), "Oda payload did not provide is_available"
    except AssertionError as exc:
        raise ApplicationError("Unable to validate Oda response") from exc
