from django.http import HttpRequest
from .records import IngredientRecord
from .models import Ingredient
from nest.audit_logs.services import log_create_or_updated


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
