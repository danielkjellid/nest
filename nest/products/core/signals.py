from typing import Any

from django.db.models.signals import pre_save
from django.dispatch import receiver

from nest.core.utils import s3_asset_cleanup
from nest.products.core.models import Product


@receiver(pre_save, sender=Product)
def delete_thumbnail_s3_asset(
    sender: Product, instance: Product, *args: Any, **kwargs: Any
) -> None:
    """
    Delete the old thumbnail if overwritten.
    """

    if instance.id is not None:
        previous_product = sender.objects.get(id=instance.id)
        if (
            previous_product.thumbnail is not None
            and previous_product.thumbnail != instance.thumbnail
        ):
            s3_asset_cleanup(instance=previous_product, field="thumbnail")
