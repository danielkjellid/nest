from typing import Iterable

from django.db.models import Q

from nest.core.types import FetchedResult
from nest.units.records import UnitRecord

from .models import RecipeIngredient, RecipeIngredientItem, RecipeIngredientItemGroup
from .records import (
    RecipeIngredientItemGroupRecord,
    RecipeIngredientItemRecord,
    RecipeIngredientRecord,
)


def get_recipe_ingredients() -> list[RecipeIngredientRecord]:
    """
    Get a list of all ingredients in the application.
    """
    ingredients = RecipeIngredient.objects.all().select_related(
        "product", "product__unit"
    )
    records = [
        RecipeIngredientRecord.from_db_model(ingredient) for ingredient in ingredients
    ]

    return records


def _get_recipe_ingredient_items(
    expression: Q | None = None,
) -> list[RecipeIngredientItem]:
    """
    Get ingredient items with all necessary prefetches to fill out a
    RecipeIngredientItemRecord.
    """

    if expression is None:
        qs = RecipeIngredientItem.objects.all()
    else:
        qs = RecipeIngredientItem.objects.filter(expression)

    ingredient_items = list(
        qs.select_related("ingredient_group", "step").prefetch_related(
            "portion_quantity_unit",
            "ingredient",
            "ingredient__product",
            "ingredient__product__unit",
        )
    )

    return ingredient_items


def get_recipe_ingredient_items_for_groups(
    *, group_ids: Iterable[int]
) -> FetchedResult[list[RecipeIngredientItemRecord]]:
    """
    Get a list of RecipeIngredientItemRecord that based on related ingredient group.
    """
    records: FetchedResult[list[RecipeIngredientItemRecord]] = {}

    for item_group_id in group_ids:
        records[item_group_id] = []

    ingredient_items = _get_recipe_ingredient_items(
        Q(ingredient_group_id__in=group_ids)
    )

    for item in ingredient_items:
        records[item.ingredient_group_id].append(
            RecipeIngredientItemRecord(
                id=item.id,
                group_title=item.ingredient_group.title,
                ingredient=RecipeIngredientRecord.from_db_model(item.ingredient),
                additional_info=item.additional_info,
                portion_quantity=item.portion_quantity,
                portion_quantity_unit=UnitRecord.from_unit(item.portion_quantity_unit),
                portion_quantity_display="{:f}".format(
                    item.portion_quantity.normalize()
                ),
            )
        )

    return records


def get_recipe_ingredient_items_for_steps(
    *, step_ids: Iterable[int]
) -> FetchedResult[list[RecipeIngredientItemRecord]]:
    """
    Get a list of RecipeIngredientItemRecord that based on related steps.
    """
    records: FetchedResult[list[RecipeIngredientItemRecord]] = {}

    for step_id in step_ids:
        records[step_id] = []

    ingredient_items = _get_recipe_ingredient_items(Q(step_id__in=step_ids))

    for item in ingredient_items:
        item_step_id = getattr(item, "step_id", None)

        if item_step_id is None:
            continue

        records[item_step_id].append(
            RecipeIngredientItemRecord(
                id=item.id,
                group_title=item.ingredient_group.title,
                ingredient=RecipeIngredientRecord.from_db_model(item.ingredient),
                additional_info=item.additional_info,
                portion_quantity=item.portion_quantity,
                portion_quantity_unit=UnitRecord.from_unit(item.portion_quantity_unit),
                portion_quantity_display="{:f}".format(
                    item.portion_quantity.normalize()
                ),
            )
        )

    return records


def get_recipe_ingredient_item_groups_for_recipes(
    *,
    recipe_ids: Iterable[int],
) -> FetchedResult[list[RecipeIngredientItemGroupRecord]]:
    """
    Get a list of ingredient item group for a list of recipes. Returns a dict where the
    recipe id is key and a list of RecipeIngredientItemGroupRecord is value.
    """
    records: FetchedResult[list[RecipeIngredientItemGroupRecord]] = {}

    # Prefill all recipes passed in so that we always return a result for them.
    for recipe_id in recipe_ids:
        records[recipe_id] = []

    item_groups = RecipeIngredientItemGroup.objects.filter(
        recipe_id__in=recipe_ids
    ).order_by("ordering")

    ingredient_items = get_recipe_ingredient_items_for_groups(
        group_ids=[item_group.id for item_group in item_groups]
    )

    for item_group in item_groups:
        records[item_group.recipe_id].append(
            RecipeIngredientItemGroupRecord(
                id=item_group.id,
                title=item_group.title,
                ordering=item_group.ordering,
                ingredient_items=ingredient_items[item_group.id],
            )
        )

    return records


def get_recipe_ingredient_item_groups_for_recipe(
    *, recipe_id: int
) -> list[RecipeIngredientItemGroupRecord]:
    """
    Get ingredient item groups for a single recipe.
    """
    ingredient_group = get_recipe_ingredient_item_groups_for_recipes(
        recipe_ids=[recipe_id]
    )

    return ingredient_group[recipe_id]
