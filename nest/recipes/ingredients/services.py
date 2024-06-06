from datetime import timedelta

from django.db import models
from django.http import HttpRequest
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING

from nest.audit_logs.services import log_create_or_updated, log_delete
from nest.core.exceptions import ApplicationError
from nest.recipes.steps.models import RecipeStep

from .models import RecipeIngredient, RecipeIngredientItem, RecipeIngredientItemGroup
from .records import RecipeIngredientRecord

if TYPE_CHECKING:
    from nest.recipes.steps.services import Step


def create_recipe_ingredient(
    *, title: str, product_id: int | str, request: HttpRequest | None = None
) -> RecipeIngredientRecord:
    """
    Create a single ingredient instance.
    """

    ingredient = RecipeIngredient(title=title, product_id=product_id)
    ingredient.full_clean()
    ingredient.save()

    log_create_or_updated(old=None, new=ingredient, request_or_user=request)
    return RecipeIngredientRecord.from_db_model(ingredient)


def delete_recipe_ingredient(
    *, pk: int | str, request: HttpRequest | None = None
) -> None:
    """
    Delete a single ingredient instance.
    """

    ingredient = RecipeIngredient.objects.get(id=pk)
    log_delete(instance=ingredient, request=request, changes={})

    ingredient.delete()


class IngredientItem(BaseModel):
    id: int | None = None
    ingredient_id: str = Field(..., alias="ingredient")
    portion_quantity: str
    portion_quantity_unit_id: str = Field(..., alias="portion_quantity_unit")
    additional_info: str | None = None


class IngredientGroupItem(BaseModel):
    id: int | None = None
    title: str
    ordering: int
    ingredient_items: list[IngredientItem]


def _get_ingredient_item_group_id(
    group_item: IngredientGroupItem,
    recipe_groups: models.QuerySet[RecipeIngredientItemGroup],
) -> int:
    return next(
        g.id
        for g in recipe_groups
        if g.title == group_item.title and g.ordering == group_item.ordering
    )


def _get_step_id_for_item(
    item: IngredientItem, steps: list["Step"], recipe_steps: models.QuerySet[RecipeStep]
) -> int | None:
    # See if we can find the Step based on the possible child in the list.
    step_for_item = next(
        (step for step in steps if item in step.ingredient_items), None
    )

    if not step_for_item:
        return None

    # If a step exists, see if we can find the related RecipeStep that is created
    # in the db.
    step = next(
        (
            s.id
            for s in recipe_steps
            if s.number == step_for_item.number
            and s.duration == timedelta(minutes=step_for_item.duration)
            and s.step_type == step_for_item.step_type
        ),
        None,
    )

    return step


def create_or_update_recipe_ingredient_items(
    recipe_id: int,
    groups: list[IngredientGroupItem],
    steps: list["Step"],
):
    ingredient_items_to_create = []
    ingredient_items_to_update = []

    recipe_groups = RecipeIngredientItemGroup.objects.filter(recipe_id=recipe_id)
    recipe_steps = RecipeStep.objects.filter(recipe_id=recipe_id)

    # All ingredient items needs to have an ingredient group, therefore, the subset of
    # all items in groups combined should make up the whole set, therefore, it makes
    # sense to use this as a starting place.
    for group in groups:
        for ingredient_item in group.ingredient_items:
            ingredient_item_id = getattr(ingredient_item, "id", None)
            correct_list = (
                ingredient_items_to_update
                if ingredient_item_id is not None
                else ingredient_items_to_create
            )

            try:
                correct_list.append(
                    RecipeIngredientItem(
                        id=ingredient_item_id,
                        ingredient_group_id=_get_ingredient_item_group_id(
                            group, recipe_groups
                        ),
                        step_id=_get_step_id_for_item(
                            ingredient_item, steps, recipe_steps
                        ),
                        ingredient_id=ingredient_item.ingredient_id,
                        additional_info=ingredient_item.additional_info,
                        portion_quantity=ingredient_item.portion_quantity,
                        portion_quantity_unit_id=ingredient_item.portion_quantity_unit_id,
                    )
                )
            except StopIteration as exc:
                raise ApplicationError(
                    message="Could not find group to connect to ingredient item."
                ) from exc

    if len(ingredient_items_to_create):
        print("create", ingredient_items_to_create)
        RecipeIngredientItem.objects.bulk_create(ingredient_items_to_create)

    if len(ingredient_items_to_update):
        print("update", ingredient_items_to_update)
        RecipeIngredientItem.objects.bulk_update(
            ingredient_items_to_update,
            fields=[
                "ingredient_group_id",
                "step_id",
                "ingredient_id",
                "portion_quantity",
                "portion_quantity_unit_id",
            ],
        )


def _validate_ingredient_item_groups(ingredient_group_items: list[IngredientGroupItem]):
    # Sanity check that we only are dealing with unique ordering properties.
    ordering = [group.ordering for group in ingredient_group_items]
    if not len(set(ordering)) == len(ordering):
        raise ApplicationError(
            message="Ordering for ingredient group items has to be unique"
        )

    # Sanity check that we are only dealing with unique instructions.
    titles = [group.title for group in ingredient_group_items]
    if not len(set(titles)) == len(titles):
        raise ApplicationError(
            message="Titles for ingredient group items has to be unique"
        )


def create_or_update_recipe_ingredient_item_groups(
    recipe_id: int,
    ingredient_item_groups: list[IngredientGroupItem],
) -> None:
    if not ingredient_item_groups:
        return None

    groups_to_create = []
    groups_to_update = []

    for item_group in ingredient_item_groups:
        item_group_id = getattr(item_group, "id", None)
        correct_list = groups_to_update if item_group_id else groups_to_create
        correct_list.append(
            RecipeIngredientItemGroup(
                recipe_id=recipe_id,
                id=item_group_id,
                title=item_group.title,
                ordering=item_group.ordering,
            )
        )

    _validate_ingredient_item_groups(
        ingredient_group_items=groups_to_update + groups_to_create
    )

    if len(groups_to_create):
        RecipeIngredientItemGroup.objects.bulk_create(groups_to_create)

    if len(groups_to_update):
        RecipeIngredientItemGroup.objects.bulk_update(
            groups_to_update,
            fields=["title", "ordering"],
        )
