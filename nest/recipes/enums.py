from django.db.models import IntegerChoices


class RecipeStatus(IntegerChoices):
    DRAFT = 1, "Draft"
    PUBLISHED = 2, "Published"


class RecipeDifficulty(IntegerChoices):
    EASY = 1, "Easy"
    MEDIUM = 2, "Medium"
    HARD = 3, "Hard"
