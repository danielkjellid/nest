from nest.products.core.models import Product
from nest.products.oda.clients import OdaClient
from nest.products.oda.records import OdaProductDetailRecord

HasBeenImportedPreviously = bool


def retrieve_product_from_oda(
    *, oda_product_id: int
) -> tuple[OdaProductDetailRecord, HasBeenImportedPreviously]:
    """
    Retrieve product from Oda and check if it has been imported previously.
    """
    oda_product = OdaClient.get_product(product_id=oda_product_id)
    has_been_imported = Product.objects.filter(oda_id=oda_product_id).exists()

    return oda_product, has_been_imported
