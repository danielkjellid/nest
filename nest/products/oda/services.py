from decimal import Decimal

import structlog
from django.core.files import File
from django.utils import timezone
from django.utils.text import slugify

from nest.core.exceptions import ApplicationError
from nest.units.selectors import get_unit_by_abbreviation, get_unit_normalized_quantity

from ..core.models import Product
from ..core.records import ProductRecord
from ..core.selectors import get_oda_product
from ..core.services import update_or_create_product
from .clients import OdaClient
from .constants import PRODUCT_NUTRITION_IDENTIFIERS
from .records import OdaProductDetailRecord

logger = structlog.getLogger()


def import_product_from_oda(*, oda_product_id: int) -> ProductRecord | None:
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
        product = get_oda_product(oda_id=product_response.id)

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
    converted_quantity, converted_unit = get_unit_normalized_quantity(
        quantity=Decimal(unit_quantity), unit=unit
    )

    # Extract nutrition values.
    nutrition = _extract_nutrition_values_from_response(
        product_response=product_response
    )
    classifiers = _extract_classifier_values_from_response(
        product_response=product_response
    )

    # A set of defaults based on our own product model.
    defaults = {
        "oda_url": product_response.front_url,
        "name": product_response.full_name,
        "gross_price": product_response.gross_price,
        "gross_unit_price": product_response.gross_unit_price,
        "unit_id": converted_unit.id,
        "unit_quantity": round(converted_quantity),
        "is_available": product_response.availability.is_available,
        "supplier": product_response.brand,
        "thumbnail": get_product_image(),
        "last_data_update": timezone.now(),
        **nutrition,
        **classifiers,
    }

    product_record = update_or_create_product(
        pk=None,
        oda_id=product_response.id,
        source="Oda",
        log_ignore_fields={"thumbnail"},
        **defaults,
    )

    return product_record


def _extract_nutrition_values_from_response(
    *, product_response: OdaProductDetailRecord
) -> dict[str, Decimal | None]:
    """
    Extract a dict of nutritional values from response record.
    """

    # The response dict that we're interested in returning. All nutrition values on the
    # product model is nullable, therefore, None is the default.
    extracted_values = PRODUCT_NUTRITION_IDENTIFIERS

    # Extract correct info from response record and map oda's keys to match our own.
    try:
        nutrition_info = product_response.detailed_info.local[
            0
        ].nutrition_info_table.rows
    except IndexError:
        return extracted_values

    nutrition_info_key_mapping = {
        "fat": "Fett",
        "fat_saturated": "hvorav mettede fettsyrer",
        "fat_monounsaturated": "hvorav enumettede fettsyrer",
        "fat_polyunsaturated": "hvorav flerumettede fettsyrer",
        "carbohydrates": "Karbohydrater",
        "carbohydrates_sugars": "hvorav sukkerarter",
        "carbohydrates_polyols": "hvorav polyoler",
        "carbohydrates_starch": "hvorav stivelse",
        "fibres": "Kostfiber",
        "protein": "Protein",
        "salt": "Salt",
        "sodium": "Natrium",
    }

    for info in nutrition_info:
        # Energy has to be treated a bit differently as the value contains the value for
        # both the kj and kcal.
        if info.key == "Energi":
            # Energy values looks like ['743', 'kJ', '/', '177', 'kcal'] after split.
            energy_values = info.value.split(" ")
            extracted_values["energy_kj"] = Decimal(energy_values[0])
            extracted_values["energy_kcal"] = Decimal(energy_values[3])
        else:
            for model_key, mapped_key in nutrition_info_key_mapping.items():
                if info.key != mapped_key:
                    continue
                # Grab the number before abbreviation. Looks something like
                # ['8.20', 'g'] after split.
                value = Decimal(info.value.split(" ")[0])
                extracted_values[model_key] = value

    return extracted_values


def _extract_classifier_values_from_response(
    *, product_response: OdaProductDetailRecord
) -> dict[str, str | None]:
    """
    Extract a dict of content values from response record.
    """
    extracted_values: dict[str, str | None] = {"ingredients": None, "allergens": None}

    try:
        contents_info = product_response.detailed_info.local[0].contents_table.rows
    except IndexError:
        return extracted_values

    for info in contents_info:
        if info.key == "Ingredienser":
            extracted_values["ingredients"] = info.value

            if info.emphasis is not None and info.emphasis.reason == "allergens":
                extracted_values["allergens"] = ", ".join(info.emphasis.keywords)

    return extracted_values


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
