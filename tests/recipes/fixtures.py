from datetime import timedelta
from decimal import Decimal
from typing import Any, TypedDict

import pytest

from nest.recipes.core.enums import RecipeDifficulty, RecipeStatus
from nest.recipes.core.models import Recipe
from nest.recipes.ingredients.models import (
    RecipeIngredient,
    RecipeIngredientItem,
    RecipeIngredientItemGroup,
)
from nest.recipes.steps.enums import RecipeStepType
from nest.recipes.steps.models import RecipeStep

##########
# Recipe #
##########


class RecipeSpec(TypedDict, total=False):
    title: str
    slug: str
    default_num_portions: int
    search_keywords: str | None
    external_id: str | None
    external_url: str | None
    status: RecipeStatus
    difficulty: RecipeDifficulty
    is_vegetarian: bool
    is_pescatarian: bool


@pytest.fixture
def default_recipe_spec() -> RecipeSpec:
    return RecipeSpec(
        title="Sample recipe",
        slug="sample-product",
        default_num_portions=4,
        search_keywords=None,
        external_id=None,
        external_url=None,
        status=RecipeStatus.PUBLISHED,
        difficulty=RecipeDifficulty.MEDIUM,
        is_vegetarian=False,
        is_pescatarian=False,
    )


@pytest.fixture
def create_recipe_from_spec(db: Any):
    def _create_recipe(spec: RecipeSpec):
        recipe, _created = Recipe.objects.get_or_create(**spec)
        return recipe

    return _create_recipe


@pytest.fixture
def recipe(
    create_instance,
    create_recipe_from_spec,
    default_recipe_spec,
):
    return create_instance(
        create_callback=create_recipe_from_spec,
        default_spec=default_recipe_spec,
        marker_name="recipe",
    )


@pytest.fixture
def recipes(create_instances, create_recipe_from_spec, default_recipe_spec):
    return create_instances(
        create_callback=create_recipe_from_spec,
        default_spec=default_recipe_spec,
        marker_name="recipes",
    )


################
# Recipe steps #
################


class RecipeStepSpec(TypedDict, total=False):
    recipe: str
    number: int
    duration: timedelta
    instruction: str
    step_type: RecipeStepType


@pytest.fixture
def default_recipe_step_spec() -> RecipeStepSpec:
    return RecipeStepSpec(
        recipe="default",
        number=1,
        duration=timedelta(minutes=5),
        instruction="A sample instruction for a recipe step.",
        step_type=RecipeStepType.COOKING,
    )


@pytest.fixture
def create_recipe_step_from_spec(db: Any, recipe, recipes, get_related_instance):
    def _create_recipe_step(spec: RecipeStepSpec):
        recipe_from_spec = get_related_instance(
            key="recipe", spec=spec, related_instance=recipe, related_instances=recipes
        )
        step, _created = RecipeStep.objects.get_or_create(
            recipe=recipe_from_spec, **spec
        )
        return step

    return _create_recipe_step


@pytest.fixture
def recipe_step(
    create_instance, create_recipe_step_from_spec, default_recipe_step_spec
):
    return create_instance(
        create_callback=create_recipe_step_from_spec,
        default_spec=default_recipe_step_spec,
        marker_name="recipe_step",
    )


@pytest.fixture
def recipe_steps(
    create_instances, create_recipe_step_from_spec, default_recipe_step_spec
):
    return create_instances(
        create_callback=create_recipe_step_from_spec,
        default_spec=default_recipe_step_spec,
        marker_name="recipe_steps",
    )


#####################
# Recipe ingredient #
#####################


class RecipeIngredientSpec(TypedDict, total=False):
    title: str
    product: str


@pytest.fixture
def default_recipe_ingredient_spec() -> RecipeIngredientSpec:
    return RecipeIngredientSpec(title="Sample ingredient", product="default")


@pytest.fixture
def create_recipe_ingredient_from_spec(
    db: Any, product, products, get_related_instance
):
    def _create_recipe_ingredient(spec: RecipeIngredientSpec):
        product_from_spec = get_related_instance(
            key="product",
            spec=spec,
            related_instance=product,
            related_instances=products,
        )
        ingredient, _created = RecipeIngredient.objects.get_or_create(
            product=product_from_spec, **spec
        )
        return ingredient

    return _create_recipe_ingredient


@pytest.fixture
def recipe_ingredient(
    create_instance, create_recipe_ingredient_from_spec, default_recipe_ingredient_spec
):
    return create_instance(
        create_callback=create_recipe_ingredient_from_spec,
        default_spec=default_recipe_ingredient_spec,
        marker_name="recipe_ingredient",
    )


@pytest.fixture
def recipe_ingredients(
    create_instances, create_recipe_ingredient_from_spec, default_recipe_ingredient_spec
):
    return create_instances(
        create_callback=create_recipe_ingredient_from_spec,
        default_spec=default_recipe_ingredient_spec,
        marker_name="recipe_ingredients",
    )


#################################
# Recipe ingredient item groups #
#################################


class RecipeIngredientItemGroupSpec(TypedDict, total=False):
    recipe: str | None
    title: str
    ordering: int


@pytest.fixture
def default_recipe_ingredient_item_group_spec() -> RecipeIngredientItemGroupSpec:
    return RecipeIngredientItemGroupSpec(
        recipe="default", title="Sample group", ordering=1
    )


@pytest.fixture
def create_recipe_ingredient_item_group_from_spec(
    db: Any, recipe, recipes, get_related_instance
):
    def _create_recipe_ingredient_item_group(spec: RecipeIngredientItemGroupSpec):
        recipe_from_spec = get_related_instance(
            key="recipe", spec=spec, related_instance=recipe, related_instances=recipes
        )
        group, _created = RecipeIngredientItemGroup.objects.get_or_create(
            recipe=recipe_from_spec, **spec
        )
        return group

    return _create_recipe_ingredient_item_group


@pytest.fixture
def recipe_ingredient_item_group(
    create_instance,
    create_recipe_ingredient_item_group_from_spec,
    default_recipe_ingredient_item_group_spec,
):
    return create_instance(
        create_callback=create_recipe_ingredient_item_group_from_spec,
        default_spec=default_recipe_ingredient_item_group_spec,
        marker_name="recipe_ingredient_item_group",
    )


@pytest.fixture
def recipe_ingredient_item_groups(
    create_instances,
    create_recipe_ingredient_item_group_from_spec,
    default_recipe_ingredient_item_group_spec,
):
    return create_instances(
        create_callback=create_recipe_ingredient_item_group_from_spec,
        default_spec=default_recipe_ingredient_item_group_spec,
        marker_name="recipe_ingredient_item_groups",
    )


##########################
# Recipe ingredient item #
##########################


class RecipeIngredientItemSpec(TypedDict, total=False):
    ingredient_group: str
    ingredient: str
    step: str
    additional_info: str | None
    portion_quantity: Decimal
    portion_quantity_unit: str


@pytest.fixture
def default_recipe_ingredient_item_spec() -> RecipeIngredientItemSpec:
    return RecipeIngredientItemSpec(
        ingredient_group="default",
        ingredient="default",
        step="default",
        additional_info=None,
        portion_quantity=Decimal("250.00"),
        portion_quantity_unit="g",
    )


@pytest.fixture
def create_recipe_ingredient_item_from_spec(
    db: Any,
    recipe_ingredient_item_group,
    recipe_ingredient_item_groups,
    recipe_ingredient,
    recipe_ingredients,
    recipe_step,
    recipe_steps,
    get_unit,
    get_related_instance,
):
    def _create_recipe_ingredient_item(spec: RecipeIngredientItemSpec):
        group_from_spec = get_related_instance(
            key="ingredient_group",
            spec=spec,
            related_instance=recipe_ingredient_item_group,
            related_instances=recipe_ingredient_item_groups,
        )
        ingredient_from_spec = get_related_instance(
            key="ingredient",
            spec=spec,
            related_instance=recipe_ingredient,
            related_instances=recipe_ingredients,
        )
        step_from_spec = get_related_instance(
            key="step",
            spec=spec,
            related_instance=recipe_step,
            related_instances=recipe_steps,
        )
        unit_from_spec = get_unit(spec.pop("portion_quantity_unit"))

        item, _created = RecipeIngredientItem.objects.get_or_create(
            ingredient_group=group_from_spec,
            ingredient=ingredient_from_spec,
            step=step_from_spec,
            portion_quantity_unit=unit_from_spec,
            **spec,
        )

        return item

    return _create_recipe_ingredient_item


@pytest.fixture
def recipe_ingredient_item(
    create_instance,
    create_recipe_ingredient_item_from_spec,
    default_recipe_ingredient_item_spec,
):
    return create_instance(
        create_callback=create_recipe_ingredient_item_from_spec,
        default_spec=default_recipe_ingredient_item_spec,
        marker_name="recipe_ingredient_item",
    )


@pytest.fixture
def recipe_ingredient_items(
    create_instances,
    create_recipe_ingredient_item_from_spec,
    default_recipe_ingredient_item_spec,
):
    return create_instances(
        create_callback=create_recipe_ingredient_item_from_spec,
        default_spec=default_recipe_ingredient_item_spec,
        marker_name="recipe_ingredient_items",
    )
