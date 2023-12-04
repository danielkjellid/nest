from nest.products.core.models import Product


def next_oda_id() -> int:
    product_highest_oda_id = Product.objects.all().order_by("-oda_id").first()
    highest_oda_id = product_highest_oda_id.oda_id if product_highest_oda_id else 1

    return highest_oda_id + 1 if highest_oda_id else 1
