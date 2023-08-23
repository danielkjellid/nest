from django.db.models import IntegerChoices

from nest.api.openapi import add_to_openapi_schema


class RecipeStatus(IntegerChoices):
    DRAFT = 1, "Draft"
    PUBLISHED = 2, "Published"


class RecipeDifficulty(IntegerChoices):
    EASY = 1, "Easy"
    MEDIUM = 2, "Medium"
    HARD = 3, "Hard"


@add_to_openapi_schema
class RecipeStepType(IntegerChoices):
    COOKING = 1, "Cooking Step"
    PREPARATION = 2, "Preparation"
