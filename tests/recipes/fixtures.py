from datetime import datetime, timedelta
from decimal import Decimal
from typing import Callable, TypedDict

import pytest
from django.utils import timezone

from nest.recipes.core.enums import RecipeDifficulty, RecipeStatus
from nest.recipes.core.models import Recipe
from nest.recipes.ingredients.models import (
    RecipeIngredient,
    RecipeIngredientItem,
    RecipeIngredientItemGroup,
)
from nest.recipes.plans.models import RecipePlan, RecipePlanItem
from nest.recipes.steps.enums import RecipeStepType
from nest.recipes.steps.models import RecipeStep, RecipeStepIngredientItem

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


CreateRecipe = Callable[[RecipeSpec], Recipe]


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
def create_recipe_from_spec(db) -> CreateRecipe:
    def _create_recipe(spec: RecipeSpec) -> Recipe:
        recipe, _created = Recipe.objects.get_or_create(**spec)
        return recipe

    return _create_recipe


@pytest.fixture
def recipe(
    create_instance,
    create_recipe_from_spec,
    default_recipe_spec,
) -> Recipe:
    return create_instance(
        create_callback=create_recipe_from_spec,
        default_spec=default_recipe_spec,
        marker_name="recipe",
    )


@pytest.fixture
def recipes(
    create_instances, create_recipe_from_spec, default_recipe_spec
) -> dict[str, Recipe]:
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


CreateRecipeStep = Callable[[RecipeStepSpec], RecipeStep]


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
def create_recipe_step_from_spec(
    db, recipe, recipes, get_related_instance
) -> CreateRecipeStep:
    def _create_recipe_step(spec: RecipeStepSpec) -> RecipeStep:
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
) -> RecipeStep:
    return create_instance(
        create_callback=create_recipe_step_from_spec,
        default_spec=default_recipe_step_spec,
        marker_name="recipe_step",
    )


@pytest.fixture
def recipe_steps(
    create_instances, create_recipe_step_from_spec, default_recipe_step_spec
) -> dict[str, RecipeStep]:
    return create_instances(
        create_callback=create_recipe_step_from_spec,
        default_spec=default_recipe_step_spec,
        marker_name="recipe_steps",
    )


class RecipeStepIngredientItemSpec(TypedDict, total=False):
    step: str
    ingredient_item: str


CreateRecipeStepIngredientItem = Callable[
    [RecipeStepIngredientItemSpec], RecipeStepIngredientItem
]


@pytest.fixture
def default_recipe_step_ingredient_item_spec() -> RecipeStepIngredientItemSpec:
    return RecipeStepIngredientItemSpec(step="default", ingredient_item="default")


@pytest.fixture
def create_recipe_step_ingredient_item_from_spec(
    db,
    recipe_step,
    recipe_steps,
    recipe_ingredient_item,
    recipe_ingredient_items,
    get_related_instance,
):
    def _create_recipe_step_ingredient_item(
        spec: RecipeStepIngredientItemSpec
    ) -> RecipeStepIngredientItem:
        step_from_spec = get_related_instance(
            key="step",
            spec=spec,
            related_instance=recipe_step,
            related_instances=recipe_steps,
        )
        ingredient_item_from_spec = get_related_instance(
            key="ingredient_item",
            spec=spec,
            related_instance=recipe_ingredient_item,
            related_instances=recipe_ingredient_items,
        )

        item, _created = RecipeStepIngredientItem.objects.get_or_create(
            step=step_from_spec,
            ingredient_item=ingredient_item_from_spec,
        )

        return item

    return _create_recipe_step_ingredient_item


@pytest.fixture
def recipe_step_ingredient_item(
    create_instance,
    create_recipe_step_ingredient_item_from_spec,
    default_recipe_step_ingredient_item_spec,
):
    return create_instance(
        create_callback=create_recipe_step_ingredient_item_from_spec,
        default_spec=default_recipe_step_ingredient_item_spec,
        marker_name="recipe_step_ingredient_item",
    )


@pytest.fixture
def recipe_step_ingredient_items(
    create_instances,
    create_recipe_step_ingredient_item_from_spec,
    default_recipe_step_ingredient_item_spec,
):
    return create_instances(
        create_callback=create_recipe_step_ingredient_item_from_spec,
        default_spec=default_recipe_step_ingredient_item_spec,
        marker_name="recipe_step_ingredient_items",
    )


#####################
# Recipe ingredient #
#####################


class RecipeIngredientSpec(TypedDict, total=False):
    title: str
    product: str
    is_base_ingredient: bool


CreateRecipeIngredient = Callable[[RecipeIngredientSpec], RecipeIngredient]


@pytest.fixture
def default_recipe_ingredient_spec() -> RecipeIngredientSpec:
    return RecipeIngredientSpec(
        title="Sample ingredient",
        product="default",
        is_base_ingredient=False,
    )


@pytest.fixture
def create_recipe_ingredient_from_spec(
    db, product, products, get_related_instance
) -> CreateRecipeIngredient:
    def _create_recipe_ingredient(spec: RecipeIngredientSpec) -> RecipeIngredient:
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
) -> RecipeIngredient:
    return create_instance(
        create_callback=create_recipe_ingredient_from_spec,
        default_spec=default_recipe_ingredient_spec,
        marker_name="recipe_ingredient",
    )


@pytest.fixture
def recipe_ingredients(
    create_instances, create_recipe_ingredient_from_spec, default_recipe_ingredient_spec
) -> dict[str, RecipeIngredient]:
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


CreateRecipeIngredientItemGroup = Callable[
    [RecipeIngredientItemGroupSpec], RecipeIngredientItemGroup
]


@pytest.fixture
def default_recipe_ingredient_item_group_spec() -> RecipeIngredientItemGroupSpec:
    return RecipeIngredientItemGroupSpec(
        recipe="default", title="Sample group", ordering=1
    )


@pytest.fixture
def create_recipe_ingredient_item_group_from_spec(
    db, recipe, recipes, get_related_instance
) -> CreateRecipeIngredientItemGroup:
    def _create_recipe_ingredient_item_group(
        spec: RecipeIngredientItemGroupSpec
    ) -> RecipeIngredientItemGroup:
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
) -> RecipeIngredientItemGroup:
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
) -> dict[str, RecipeIngredientItemGroup]:
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
    additional_info: str | None
    portion_quantity: Decimal
    portion_quantity_unit: str


CreateRecipeIngredientItem = Callable[[RecipeIngredientItemSpec], RecipeIngredientItem]


@pytest.fixture
def default_recipe_ingredient_item_spec() -> RecipeIngredientItemSpec:
    return RecipeIngredientItemSpec(
        ingredient_group="default",
        ingredient="default",
        additional_info=None,
        portion_quantity=Decimal("250.00"),
        portion_quantity_unit="g",
    )


@pytest.fixture
def create_recipe_ingredient_item_from_spec(
    db,
    recipe_ingredient_item_group,
    recipe_ingredient_item_groups,
    recipe_ingredient,
    recipe_ingredients,
    get_unit,
    get_related_instance,
) -> CreateRecipeIngredientItem:
    def _create_recipe_ingredient_item(
        spec: RecipeIngredientItemSpec
    ) -> RecipeIngredientItem:
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
        unit_from_spec = get_unit(spec.pop("portion_quantity_unit"))

        item, _created = RecipeIngredientItem.objects.get_or_create(
            ingredient_group=group_from_spec,
            ingredient=ingredient_from_spec,
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
) -> RecipeIngredientItem:
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
) -> dict[str, RecipeIngredientItem]:
    return create_instances(
        create_callback=create_recipe_ingredient_item_from_spec,
        default_spec=default_recipe_ingredient_item_spec,
        marker_name="recipe_ingredient_items",
    )


###############
# Recipe plan #
###############


class RecipePlanSpec(TypedDict, total=False):
    title: str
    description: str | None
    slug: str
    home: str
    from_date: datetime


CreateRecipePlan = Callable[[RecipePlanSpec], RecipePlan]


@pytest.fixture
def default_recipe_plan_spec() -> RecipePlanSpec:
    return RecipePlanSpec(
        title="Recipe test plan",
        description=None,
        home="default",
        slug="recipe-test-plan",
        from_date=timezone.now(),
    )


@pytest.fixture
def create_recipe_plan_from_spec(
    db, get_related_instance, home, homes
) -> CreateRecipePlan:
    def _create_recipe_plan(spec: RecipePlanSpec) -> RecipePlan:
        home_from_spec = get_related_instance(
            key="home", spec=spec, related_instance=home, related_instances=homes
        )
        recipe_plan, _created = RecipePlan.objects.get_or_create(
            home=home_from_spec, **spec
        )
        return recipe_plan

    return _create_recipe_plan


@pytest.fixture
def recipe_plan(
    create_instance,
    create_recipe_plan_from_spec,
    default_recipe_plan_spec,
) -> RecipePlan:
    return create_instance(
        create_callback=create_recipe_plan_from_spec,
        default_spec=default_recipe_plan_spec,
        marker_name="recipe_plan",
    )


@pytest.fixture
def recipe_plans(
    create_instances, create_recipe_plan_from_spec, default_recipe_plan_spec
) -> dict[str, RecipePlan]:
    return create_instances(
        create_callback=create_recipe_plan_from_spec,
        default_spec=default_recipe_plan_spec,
        marker_name="recipe_plans",
    )


#####################
# Recipe plan items #
#####################


class RecipePlanItemSpec(TypedDict, total=False):
    recipe_plan: str
    recipe: str
    ordering: int


CreateRecipePlanItem = Callable[[RecipePlanItemSpec], RecipePlanItem]


@pytest.fixture
def default_recipe_plan_item_spec() -> RecipePlanItemSpec:
    return RecipePlanItemSpec(recipe_plan="default", recipe="default", ordering=1)


@pytest.fixture
def create_recipe_plan_item_from_spec(
    db, recipe_plan, recipe_plans, recipe, recipes, get_related_instance
) -> CreateRecipePlanItem:
    def _create_recipe_plan_item(spec: RecipePlanItemSpec) -> RecipePlanItem:
        recipe_plan_from_spec = get_related_instance(
            key="recipe_plan",
            spec=spec,
            related_instance=recipe_plan,
            related_instances=recipe_plans,
        )
        recipe_from_spec = get_related_instance(
            key="recipe",
            spec=spec,
            related_instance=recipe,
            related_instances=recipes,
        )
        recipe_plan_item, _created = RecipePlanItem.objects.get_or_create(
            recipe=recipe_from_spec, recipe_plan=recipe_plan_from_spec, **spec
        )

        return recipe_plan_item

    return _create_recipe_plan_item


@pytest.fixture
def recipe_plan_item(
    create_instance, create_recipe_plan_item_from_spec, default_recipe_plan_item_spec
):
    return create_instance(
        create_callback=create_recipe_plan_item_from_spec,
        default_spec=default_recipe_plan_item_spec,
        marker_name="recipe_plan_item",
    )


@pytest.fixture
def recipe_plan_items(
    create_instances, create_recipe_plan_item_from_spec, default_recipe_plan_item_spec
) -> dict[str, RecipePlanItem]:
    return create_instances(
        create_callback=create_recipe_plan_item_from_spec,
        default_spec=default_recipe_plan_item_spec,
        marker_name="recipe_plan_items",
    )
