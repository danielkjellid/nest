import functools
from decimal import Decimal

from django.db import transaction
from django.http import HttpRequest
from pydantic import BaseModel, Field

from nest.audit_logs.services import log_create_or_updated, log_delete
from nest.core.exceptions import ApplicationError

from .models import RecipeIngredient, RecipeIngredientItem, RecipeIngredientItemGroup
from .records import RecipeIngredientRecord


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


@transaction.atomic
def _create_or_update_recipe_ingredient_items(
    recipe_id: int,
    ingredient_item_groups: list[IngredientGroupItem],
):
    item_groups = RecipeIngredientItemGroup.objects.filter(recipe_id=recipe_id)

    ingredient_items_to_create = []
    ingredient_items_to_update = []

    def build_ingredient_item(
        groups: list[RecipeIngredientItemGroup],
        group_item: IngredientGroupItem,
        ingredient_item: IngredientItem,
    ) -> RecipeIngredientItem:
        try:
            return RecipeIngredientItem(
                id=getattr(ingredient_item, "id", None),
                ingredient_group_id=next(
                    group.id
                    for group in groups
                    if group.title == group_item.title
                    and group.ordering == group_item.ordering
                ),
                ingredient_id=ingredient_item.ingredient_id,
                additional_info=ingredient_item.additional_info,
                portion_quantity=Decimal(ingredient_item.portion_quantity),
                portion_quantity_unit_id=ingredient_item.portion_quantity_unit_id,
            )
        except StopIteration as exc:
            raise ApplicationError(
                message="Could not find group to connect to ingredient item."
            ) from exc

    for group_item in ingredient_item_groups:
        for ingredient_item in group_item.ingredient_items:
            correct_list = (
                ingredient_items_to_update
                if getattr(ingredient_item, "id", None)
                else ingredient_items_to_create
            )
            correct_list.append(
                build_ingredient_item(
                    groups=item_groups,
                    group_item=group_item,
                    ingredient_item=ingredient_item,
                )
            )

    def modify_ingredient_items() -> None:
        if len(ingredient_items_to_create):
            RecipeIngredientItem.objects.bulk_create(ingredient_items_to_create)

        if len(ingredient_items_to_update):
            RecipeIngredientItem.objects.bulk_update(
                ingredient_items_to_update,
                fields=[
                    "ingredient_group_id",
                    "ingredient_id",
                    "portion_quantity",
                    "portion_quantity_unit_id",
                ],
            )

    transaction.on_commit(modify_ingredient_items)


@transaction.atomic
def create_or_update_recipe_ingredient_item_groups(
    recipe_id: int,
    ingredient_item_groups: list[IngredientGroupItem],
) -> None:
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

    transaction.on_commit(
        functools.partial(
            _create_or_update_recipe_ingredient_items,
            recipe_id=recipe_id,
            ingredient_item_groups=ingredient_item_groups,
        )
    )
