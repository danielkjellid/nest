from decimal import Decimal
from io import BytesIO

from django.core.files.images import ImageFile
from PIL import Image

from nest.products.models import Product
from nest.units.models import Unit
from nest.units.tests.utils import get_unit


def create_product_image(
    *, name: str, extension: str = "jpeg", width: int = 300, height: int = 300
) -> ImageFile:
    """
    Create a product image file to use in tests.
    """

    file = BytesIO()
    image = Image.new("L", size=(width, height))
    image.save(file, extension.lower())
    file.name = f"{name}.{extension.lower()}"
    file.seek(0)

    return ImageFile(file)


def next_oda_id() -> int:
    product_highest_oda_id = Product.objects.all().order_by("-oda_id").first()
    highest_oda_id = product_highest_oda_id.oda_id if product_highest_oda_id else 1

    return highest_oda_id + 1


def create_product(
    *,
    name: str | None = "Test product",
    gross_price: str | None = "100.00",
    unit_quantity: str | None = "1.00",
    unit: Unit | None = None,
    oda_id: int | None = None,
    is_available: bool = True,
    is_synced: bool = True,
) -> Product:
    if unit is None:
        unit = get_unit()

    if oda_id is None:
        oda_id = next_oda_id()

    unit_price = str(float(gross_price) / float(unit_quantity))

    product, _created = Product.objects.get_or_create(
        name=name,
        oda_id=oda_id,
        defaults={
            "gross_price": Decimal(gross_price),
            "gross_unit_price": Decimal(unit_price),
            "unit": unit,
            "unit_quantity": Decimal(unit_quantity),
            "oda_url": f"https://example.com/{oda_id}/",
            "is_available": is_available,
            "gtin": "01234567891234",
            "supplier": "Example supplier",
            "is_synced": is_synced,
        },
    )

    product.thumbnail.save("thumbnail.jpg", create_product_image(name="thumbnail"))

    return product
