from .records import RecipeIngredientRecord
from .models import RecipeIngredient
from nest.audit_logs.services import log_create_or_updated
from django.http import HttpRequest


def create_ingredient(
    *, title: str, product_id: int | str, request: HttpRequest | None = None
) -> RecipeIngredientRecord:
    """
    Create a single ingredient instance.
    """

    ingredient = RecipeIngredient(title=title, product_id=product_id)
    ingredient.full_clean()
    ingredient.save()

    log_create_or_updated(old=None, new=ingredient, request_or_user=request)
    return RecipeIngredientRecord.from_ingredient(ingredient=ingredient)
