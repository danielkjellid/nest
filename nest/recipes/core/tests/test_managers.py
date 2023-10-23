from datetime import timedelta

import pytest

from nest.recipes.steps.enums import RecipeStepType
from ..models import Recipe
from .utils import create_recipe
from nest.recipes.steps.tests.utils import create_recipe_step

pytestmark = pytest.mark.django_db


class TestRecipeQuerySet:
    def test_manager_annotate_duration(self, django_assert_num_queries):
        """
        Test that the annotate_duration manager correctly annotates duration values.
        """
        recipe = create_recipe()

        step1_duration = 5
        create_recipe_step(
            recipe=recipe, duration=step1_duration, step_type=RecipeStepType.PREPARATION
        )

        step2_duration = 5
        create_recipe_step(
            recipe=recipe, duration=step2_duration, step_type=RecipeStepType.COOKING
        )

        step3_duration = 10
        create_recipe_step(
            recipe=recipe, duration=step3_duration, step_type=RecipeStepType.COOKING
        )

        with django_assert_num_queries(1):
            recipe_with_duration = (
                Recipe.objects.filter(id=recipe.id).annotate_duration().first()
            )

        assert hasattr(recipe_with_duration, "preparation_time")
        assert hasattr(recipe_with_duration, "cooking_time")
        assert hasattr(recipe_with_duration, "total_time")

        assert recipe_with_duration.preparation_time == timedelta(
            seconds=step1_duration * 60
        )
        assert recipe_with_duration.cooking_time == timedelta(
            seconds=(step2_duration + step3_duration) * 60
        )
        assert recipe_with_duration.total_time == timedelta(
            seconds=(step1_duration + step2_duration + step3_duration) * 60
        )
