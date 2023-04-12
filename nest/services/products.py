from nest.clients import OdaClient
from nest.records import OdaProductDetailRecord, ProductRecord
from nest.selectors import UnitSelector, ProductSelector
from nest.exceptions import ApplicationError
import structlog
from nest.models import Product
from typing import Any

logger = structlog.getLogger()


class ProductService:
    def __init__(self) -> None:
        ...

    @classmethod
    def update_or_create_product(
        cls, *, pk: int | None = None, oda_id: int | None = None, **kwargs: Any
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

    @classmethod
    def import_from_oda(cls, oda_product_id: int) -> ProductRecord | None:
        """
        Import a product from Oda based on the Oda product id.
        """

        # Get product data and image from Oda API.
        product_response = OdaClient.get_product(product_id=oda_product_id)
        product_image = OdaClient.get_image(
            url=product_response.images[0].thumbnail.url, filename="thumbnail.jpg"
        )

        # Validate that all required values are present.
        cls._validate_oda_response(response_record=product_response)

        # Some products can be excluded from the sync, if so, we want to early return.
        # The selector will throw an Application error if the product does not exit, so
        # we deliberately catch it and ignore it here.
        try:
            product = ProductSelector.get_product(oda_id=product_response.id)

            if not getattr(product, "is_synced", True):
                return
        except ApplicationError:
            pass

        # Get corresponding unit from product response
        unit = UnitSelector.get_unit_from_abbreviation(
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

        product_record = cls.update_or_create_product(
            oda_id=product_response.id, **defaults
        )

        if product_image:
            product = ProductSelector._get_product(pk=product_record.id)
            product.thumbnail.save("thumbnail.jpg", product_image)

        return ProductRecord.from_product(product)

    @staticmethod
    def _validate_oda_response(response_record: OdaProductDetailRecord):
        """
        Validate that required values from the Oda product response is present, and
        raise an exception if they're not.
        """
        try:
            assert response_record.id, "Oda payload did not provide an id"
            assert response_record.full_name, "Oda payload did not provide a name"
            assert (
                response_record.gross_price
            ), "Oda payload did not provide a gross_price"
            assert (
                response_record.unit_price_quantity_abbreviation
            ), "Oda payload did not provide a unit abbreviation"
            assert response_record.brand, "Oda payload did not provide a supplier"
            assert (
                response_record.availability.is_available is not None
            ), "Oda payload did not provide is_available"
        except AssertionError as exc:
            raise ApplicationError("Unable to validate Oda response") from exc
