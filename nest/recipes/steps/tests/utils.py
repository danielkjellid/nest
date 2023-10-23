from ..models import RecipeStep
from ..enums import RecipeStepType
from nest.recipes.core.models import Recipe
from nest.recipes.core.tests.utils import create_recipe
from datetime import timedelta


def create_recipe_step(
    *,
    recipe: Recipe | None = None,
    number: int = 1,
    duration: int = 5,
    instruction: str = "Instruction for step",
    step_type: RecipeStep = RecipeStepType.COOKING,
) -> RecipeStep:
    """
    Create a recipe step to use in tests.
    """
    if not recipe:
        recipe = create_recipe()

    step = RecipeStep.objects.create(
        recipe=recipe,
        number=number,
        duration=timedelta(minutes=duration),
        instruction=instruction,
        step_type=step_type,
    )

    return step
