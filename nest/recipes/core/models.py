from django.db import models

from nest.core.models import BaseModel

from .enums import RecipeDifficulty, RecipeStatus
from .managers import RecipeQuerySet

_RecipeManager = models.Manager.from_queryset(RecipeQuerySet)


class Recipe(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50)
    default_num_portions = models.PositiveIntegerField(default=4)
    search_keywords = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Separate with spaces. Title is included by default.",
    )

    external_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Recipe identifier on a provider's site",
    )
    external_url = models.URLField(
        null=True,
        blank=True,
        help_text="Direct link to the recipe on a provider's site",
    )

    status = models.CharField(
        choices=RecipeStatus.choices, default=RecipeStatus.DRAFT, max_length=20
    )
    difficulty = models.CharField(
        choices=RecipeDifficulty.choices, default=RecipeDifficulty.EASY, max_length=20
    )
    is_vegetarian = models.BooleanField(default=False)
    is_pescatarian = models.BooleanField(default=False)

    objects = _RecipeManager()

    class Meta:
        verbose_name = "recipe"
        verbose_name_plural = "recipes"

    def __str__(self) -> str:
        return f"{self.title} ({self.id})"
