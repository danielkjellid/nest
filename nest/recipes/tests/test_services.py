import pytest
import nest.recipes.tests.utils as utils
from nest.products.tests.utils import create_product
from nest.ingredients.tests.utils import create_ingredient
from ..models import RecipeStep, RecipeIngredientItemGroup, RecipeIngredientItem, Recipe
from ..services import create_recipe_steps, create_ingredient_item_groups, create_recipe
from nest.units.tests.utils import get_unit
from nest.core.exceptions import ApplicationError
from ..enums import RecipeDifficulty, RecipeStatus

pytestmark = pytest.mark.django_db


class TestRecipeServices:
    def test_service_create_recipe(self, django_assert_num_queries):
        """
        Test that the create_recipe service successfully creates a recipe with expected
        output.
        """

        assert Recipe.objects.count() == 0

        fields = {
            "title": "A new recipe",
            "default_num_portions": 3,
            "status": "1",
            "difficulty": RecipeDifficulty.MEDIUM,
            "is_vegetarian": True,
        }

        with django_assert_num_queries(3):
            recipe = create_recipe(**fields)

        assert Recipe.objects.count() == 1

        assert recipe.title == fields["title"]
        assert recipe.default_num_portions == fields["default_num_portions"]
        assert recipe.status == RecipeStatus.DRAFT
        assert recipe.difficulty == RecipeDifficulty.MEDIUM
        assert recipe.is_vegetarian is True
        assert recipe.external_id is None
        assert recipe.external_url is None

    def test_service_create_ingredient_item_groups(
        self, immediate_on_commit, django_assert_num_queries
    ):
        """
        Test that creating ingredient item groups using the create_ingredient_item_groups
        service works as expected within query limits.
        """
        recipe = utils.create_recipe()
        payload = [
            {
                "title": "Cod with peppers",
                "ordering": 1,
                "ingredients": [
                    {
                        "ingredient_id": create_ingredient(
                            title="Green peppers",
                            product=create_product(name="Peppers, green"),
                        ).id,
                        "additional_info": None,
                        "portion_quantity": "100",
                        "portion_quantity_unit_id": get_unit("g").id,
                    },
                    {
                        "ingredient_id": create_ingredient(
                            title="Cod", product=create_product(name="Fresh luxury cod")
                        ).id,
                        "additional_info": "Descaled",
                        "portion_quantity": "1",
                        "portion_quantity_unit_id": get_unit("kg").id,
                    },
                ],
            },
            {
                "title": "Accessories",
                "ordering": 2,
                "ingredients": [
                    {
                        "ingredient_id": create_ingredient(
                            title="Parsly",
                            product=create_product(name="Fresh parsly"),
                        ).id,
                        "additional_info": None,
                        "portion_quantity": "20",
                        "portion_quantity_unit_id": get_unit("g").id,
                    }
                ],
            },
        ]

        assert RecipeIngredientItemGroup.objects.count() == 0
        assert RecipeIngredientItem.objects.count() == 0

        with immediate_on_commit, django_assert_num_queries(4):
            create_ingredient_item_groups(
                recipe_id=recipe.id, ingredient_group_items=payload
            )

        item_groups = RecipeIngredientItemGroup.objects.all().order_by("ordering")

        assert len(item_groups) == 2

        assert item_groups[0].recipe_id == recipe.id
        assert item_groups[0].title == payload[0]["title"]
        assert item_groups[0].ordering == payload[0]["ordering"]
        assert set(
            item_groups[0].ingredient_items.all().values_list("id", flat=True)
        ) == set(item["ingredient_id"] for item in payload[0]["ingredients"])

        assert item_groups[1].recipe_id == recipe.id
        assert item_groups[1].title == payload[1]["title"]
        assert item_groups[1].ordering == payload[1]["ordering"]
        assert set(
            item_groups[1].ingredient_items.all().values_list("id", flat=True)
        ) == set(item["ingredient_id"] for item in payload[1]["ingredients"])

        # Test that ApplicationError is raised when ordering is not unique.
        with pytest.raises(ApplicationError):
            create_ingredient_item_groups(
                recipe_id=recipe.id,
                ingredient_group_items=[
                    {
                        "title": "Cod with peppers",
                        "ordering": 1,
                        "ingredients": [],
                    },
                    {
                        "title": "Accessories",
                        "ordering": 1,
                        "ingredients": [],
                    },
                ],
            )

        # Test that ApplicationError is raised when title is not unique.
        with pytest.raises(ApplicationError):
            create_ingredient_item_groups(
                recipe_id=recipe.id,
                ingredient_group_items=[
                    {
                        "title": "Cod with peppers",
                        "ordering": 1,
                        "ingredients": [],
                    },
                    {
                        "title": "Cod with peppers",
                        "ordering": 2,
                        "ingredients": [],
                    },
                ],
            )

    def test_service_create_recipe_steps(self, django_assert_num_queries):
        """
        Test that creating steps using the create_recipe_steps service works as expected
        within query limits.
        """
        recipe = utils.create_recipe()
        item_group_1 = utils.create_recipe_ingredient_item_group(
            title="Cod with peppers"
        )
        item_group_2 = utils.create_recipe_ingredient_item_group(title="Accessories")

        payload = [
            {
                "number": 1,
                "duration": 5,
                "instruction": "Some instruction for step 1",
                "step_type": "2",
                "ingredient_items": [
                    utils.create_recipe_ingredient_item(
                        ingredient_group=item_group_1,
                        ingredient=create_ingredient(
                            title="Green peppers",
                            product=create_product(name="Peppers, green"),
                        ),
                    ).id,
                    utils.create_recipe_ingredient_item(
                        ingredient_group=item_group_1,
                        ingredient=create_ingredient(
                            title="Cod", product=create_product(name="Fresh luxury cod")
                        ),
                    ).id,
                    utils.create_recipe_ingredient_item(
                        ingredient_group=item_group_2,
                        ingredient=create_ingredient(
                            title="Parsly",
                            product=create_product(name="Fresh parsly"),
                        ),
                    ).id,
                ],
            },
            {
                "number": 2,
                "duration": 3,
                "instruction": "Some instruction for step 2",
                "step_type": "2",
                "ingredient_items": [
                    utils.create_recipe_ingredient_item(
                        ingredient_group=item_group_2,
                        ingredient=create_ingredient(
                            title="Salt",
                            product=create_product(name="Kosher salt"),
                        ),
                    ).id,
                ],
            },
        ]

        assert RecipeStep.objects.count() == 0

        with django_assert_num_queries(3):
            create_recipe_steps(recipe_id=recipe.id, steps=payload)

        recipe_steps = RecipeStep.objects.all().order_by("number")

        assert len(recipe_steps) == 2

        assert recipe_steps[0].recipe_id == recipe.id
        assert recipe_steps[0].number == payload[0]["number"]
        assert recipe_steps[0].instruction == payload[0]["instruction"]
        assert set(
            recipe_steps[0].ingredient_items.all().values_list("id", flat=True)
        ) == set(payload[0]["ingredient_items"])

        assert recipe_steps[1].recipe_id == recipe.id
        assert recipe_steps[1].number == payload[1]["number"]
        assert recipe_steps[1].instruction == payload[1]["instruction"]
        assert set(
            recipe_steps[1].ingredient_items.all().values_list("id", flat=True)
        ) == set(payload[1]["ingredient_items"])

        # Test that application error is raised if number is off sequence.
        with pytest.raises(ApplicationError):
            create_recipe_steps(
                recipe_id=recipe.id,
                steps=[
                    {
                        "number": 1,
                        "duration": 1,
                        "instruction": "Some instruction",
                        "step_type": "2",
                        "ingredient_items": [],
                    },
                    {
                        "number": 3,
                        "duration": 1,
                        "instruction": "Some instruction",
                        "step_type": "2",
                        "ingredient_items": [],
                    },
                ],
            )

        # Test that ApplicationError is raised if number: 1 is not present in payload.
        with pytest.raises(ApplicationError):
            create_recipe_steps(
                recipe_id=recipe.id,
                steps=[
                    {
                        "number": 2,
                        "duration": 1,
                        "instruction": "Some instruction",
                        "step_type": "2",
                        "ingredient_items": [],
                    },
                    {
                        "number": 3,
                        "duration": 1,
                        "instruction": "Some instruction",
                        "step_type": "2",
                        "ingredient_items": [],
                    },
                ],
            )

        # Test that ApplicationError is raised if any of the instructions is empty.
        with pytest.raises(ApplicationError):
            create_recipe_steps(
                recipe_id=recipe.id,
                steps=[
                    {
                        "number": 1,
                        "duration": 1,
                        "instruction": "",
                        "step_type": "2",
                        "ingredient_items": [],
                    },
                    {
                        "number": 1,
                        "duration": 1,
                        "instruction": "Some instruction",
                        "step_type": "2",
                        "ingredient_items": [],
                    },
                ],
            )
