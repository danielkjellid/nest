from django.db.models import TextChoices


class RecipeStepType(TextChoices):
    COOKING = "cooking", "Cooking Step"
    PREPARATION = "preparation", "Preparation"
