from django.http import HttpRequest

from nest.audit_logs.services import log_create_or_updated

from .models import Ingredient
from .records import IngredientRecord


def create_ingredient(
    *, title: str, product_id: int | str, request: HttpRequest | None = None
) -> IngredientRecord:
    """
    Create a single ingredient instance.
    """

    ingredient = Ingredient(title=title, product_id=product_id)
    ingredient.full_clean()
    ingredient.save()

    log_create_or_updated(old=None, new=ingredient, request_or_user=request)
    return IngredientRecord.from_ingredient(ingredient)
