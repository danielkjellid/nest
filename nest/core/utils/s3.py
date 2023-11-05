from typing import TypeVar

from django.conf import settings
from django.db.models import Model
from django.db.models.fields.files import FieldFile, ImageFieldFile
from django_s3_storage.storage import S3Storage

T_MODEL = TypeVar("T_MODEL", bound=Model)


def s3_asset_delete(*, storage_key: str | None = None) -> None:
    """
    Delete s3 assets based on storage key.
    """

    if not storage_key:
        raise ValueError(
            "Storage key cannot be empty, to able to cleanup remote folder."
        )

    storage = S3Storage(aws_s3_bucket_name=settings.AWS_S3_BUCKET_NAME)
    parent_path_key = storage_key.rsplit("/", 1)[0]  # Get everything before the last /

    if storage.exists(parent_path_key):
        dirs, files = storage.listdir(parent_path_key)

        if len(dirs) == 0 and len(files) == 0:
            storage.delete(parent_path_key)


def s3_asset_cleanup(*, instance: T_MODEL, field: str) -> None:
    """
    Delete specific s3 assets belonging to an instance.
    """

    instance_field = getattr(instance, field, None)

    if instance_field and isinstance(instance_field, (ImageFieldFile, FieldFile)):
        storage_key = instance_field.name
        instance_field.delete(save=False)

        s3_asset_delete(storage_key=storage_key)
