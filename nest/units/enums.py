from django.db.models import TextChoices

from nest.api.openapi import add_to_openapi_schema


@add_to_openapi_schema
class UnitType(TextChoices):
    PIECES = "pieces", "Pieces"
    WEIGHT = "weight", "Weight"
    VOLUME = "volume", "Volume"
    LENGTH = "length", "Length"
    USAGE = "usage", "Usage"
