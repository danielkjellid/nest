import structlog
from django.core.files import File
from django.utils.text import slugify

from nest.core.exceptions import ApplicationError
from nest.data_pools.providers.oda.clients import OdaClient
from nest.data_pools.providers.oda.records import OdaProductDetailRecord
from nest.units.selectors import get_unit_by_abbreviation

from ..models import Product
from ..records import ProductRecord
from ..selectors import get_product
from .core import update_or_create_product

logger = structlog.getLogger()


def import_from_oda(*, oda_product_id: int) -> ProductRecord | None:
    """
    Import a product from Oda based on the Oda product id.
    """

    # Get product data and image from Oda API.
    product_response = OdaClient.get_product(product_id=oda_product_id)
    product_image = OdaClient.get_image(
        url=product_response.images[0].thumbnail.url, filename="thumbnail.jpg"
    )

    def get_product_image() -> File | None:  # type: ignore
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
