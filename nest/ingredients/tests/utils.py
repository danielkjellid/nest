from ..models import Ingredient
from nest.products.tests.utils import create_product
from nest.products.models import Product


def create_ingredient(
    *, title: str = "Test ingredient", product: Product | None = None
) -> Ingredient:
    """
    Create a recipe ingredient to use in tests.
    """
    if not product:
        product = create_product()

    ingredient, _created = Ingredient.objects.get_or_create(
        title=title, product=product
    )

    return ingredient
