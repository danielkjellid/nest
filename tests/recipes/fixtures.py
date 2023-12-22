from typing import Any, Callable, TypedDict

import pytest

from nest.products.core.models import Product
from nest.recipes.core.enums import RecipeDifficulty, RecipeStatus
from nest.recipes.core.models import Recipe
from nest.recipes.ingredients.models import RecipeIngredient

from ..factories.fixtures import (
    get_instance,
    get_spec_for_instance,
    instance,
    instances,
)
from ..products.fixtures import ProductSpec


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
def create_recipe(db: Any) -> CreateRecipe:
    """
    Creates a single recipe.

    This function does not provide any defaults, so everything needed has to be
    specified. You should probably use the get_recipe fixture instead.
    """

    def _create_recipe(spec: RecipeSpec) -> Recipe:
        recipe = Recipe.objects.create(**spec)
        return recipe

    return _create_recipe


@pytest.fixture
def default_recipe_spec(request: pytest.FixtureRequest) -> RecipeSpec:
    """
    Get the default spec for a recipe.
    """

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
def get_recipe_spec(
    default_recipe_spec: RecipeSpec, request: pytest.FixtureRequest
) -> RecipeSpec:
    """
    Replace spec defaults with kwargs passed in marker.
    """

    def _get_recipe_spec(slug: str) -> RecipeSpec:
        return get_spec_for_instance(
            slug=slug,
            default_spec=default_recipe_spec,
            request=request,
            marker="recipes",
        )

    return _get_recipe_spec


@pytest.fixture
def get_recipe(
    create_recipe: CreateRecipe,
    get_recipe_spec: Callable[[str], RecipeSpec],
) -> Callable[[str], Recipe]:
    recipes: dict[str, Recipe] = {}

    def get_or_create_recipe(slug: str) -> Recipe:
        return get_instance(
            slug=slug,
            instances=recipes,
            create_callback=create_recipe,
            get_spec_callback=get_recipe_spec,
        )

    return get_or_create_recipe


@pytest.fixture
def recipe(
    request: pytest.FixtureRequest,
    create_recipe: CreateRecipe,
    default_recipe_spec: RecipeSpec,
) -> Recipe:
    return instance(
        create_callback=create_recipe,
        default_spec=default_recipe_spec,
        request=request,
        marker="recipe",
    )


@pytest.fixture
def recipes(
    get_recipe: Callable[[str], Recipe], request: pytest.FixtureRequest
) -> dict[str, Recipe]:
    return instances(
        request=request, markers="recipes", get_instance_callback=get_recipe
    )


class RecipeIngredientSpec(TypedDict, total=False):
    title: str
    product: dict[str, ProductSpec]


CreateRecipeIngredient = Callable[[RecipeIngredientSpec], RecipeIngredient]


@pytest.fixture
def create_recipe_ingredient(
    db: Any, get_product: Callable[[str], Product]
) -> CreateRecipeIngredient:
    """
    Creates a single recipe ingredient.

    This function does not provide any defaults, so everything needed has to be
    specified. You should probably use the get_recipe_ingredient fixture instead.
    """

    def _create_recipe_ingredient(spec: RecipeIngredientSpec) -> RecipeIngredient:
        product_from_spec = get_product(spec["product"])

        recipe_ingredient = RecipeIngredient.objects.create(
            title=spec["title"], product=product_from_spec
        )
        return recipe_ingredient

    return _create_recipe_ingredient


@pytest.fixture
def default_recipe_ingredient_spec(
    request: pytest.FixtureRequest, product: Product
) -> RecipeIngredientSpec:
    """
    Get the default spec for a recipe ingredient,
    """
    return RecipeIngredientSpec(title="Sample ingredient", product=product)


@pytest.fixture
def get_recipe_ingredient_spec(
    default_recipe_ingredient_spec: RecipeIngredientSpec, request: pytest.FixtureRequest
) -> RecipeIngredientSpec:
    """
    Replace spec defaults with kwargs passed in marker.
    """

    def _get_recipe_ingredient_spec(slug: str) -> RecipeIngredientSpec:
        return get_spec_for_instance(
            slug=slug,
            default_spec=default_recipe_ingredient_spec,
            request=request,
            marker="recipe_ingredients",
        )

    return _get_recipe_ingredient_spec


@pytest.fixture
def get_recipe_ingredient(
    create_recipe_ingredient: CreateRecipeIngredient,
    get_recipe_ingredient_spec: Callable[[str], RecipeIngredientSpec],
) -> Callable[[str], RecipeIngredient]:
    recipe_ingredients: dict[str, RecipeIngredient] = {}

    def get_or_create_recipe_ingredient(slug: str) -> RecipeIngredient:
        return get_instance(
            slug=slug,
            instances=recipe_ingredients,
            create_callback=create_recipe_ingredient,
            get_spec_callback=get_recipe_ingredient_spec,
        )

    return get_or_create_recipe_ingredient


@pytest.fixture
def recipe_ingredient(
    request: pytest.FixtureRequest,
    create_recipe_ingredient: CreateRecipeIngredient,
    default_recipe_ingredient_spec: RecipeIngredientSpec,
) -> RecipeIngredient:
    return instance(
        create_callback=create_recipe_ingredient,
        default_spec=default_recipe_ingredient_spec,
        request=request,
        marker="recipe_ingredient",
    )


@pytest.fixture
def recipe_ingredients(
    get_recipe_ingredient: Callable[[str], RecipeIngredient],
    request: pytest.FixtureRequest,
) -> dict[str, RecipeIngredient]:
    return instances(
        request=request,
        markers="recipe_ingredients",
        get_instance_callback=get_recipe_ingredient,
    )
