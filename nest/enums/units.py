from django.db.models import TextChoices


class Unit(TextChoices):
    PIECES = "pieces", "Pieces"
    WEIGHT = "weight", "Weight"
    VOLUME = "volume", "Volume"
    LENGTH = "length", "Length"
    USAGE = "usage", "Usage"
