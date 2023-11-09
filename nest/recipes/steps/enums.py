from django.db.models import TextChoices
from nest.api.openapi import add_to_openapi_schema


@add_to_openapi_schema
class RecipeStepType(TextChoices):
    COOKING = "cooking", "Cooking Step"
    PREPARATION = "preparation", "Preparation"
