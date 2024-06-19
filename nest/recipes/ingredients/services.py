import functools

import structlog
from django.db import models, transaction
from django.http import HttpRequest
from pydantic import BaseModel, Field

from nest.audit_logs.services import log_create_or_updated, log_delete
from nest.core.exceptions import ApplicationError

from .models import RecipeIngredient, RecipeIngredientItem, RecipeIngredientItemGroup
from .records import RecipeIngredientRecord

logger = structlog.get_logger()


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


def create_or_update_recipe_ingredient_items(
    recipe_id: int,
    groups: list[IngredientGroupItem],
) -> None:
    logger.info("Creating and updating ingredient items")

    ingredient_items_to_create: list[RecipeIngredientItem] = []
    ingredient_items_to_update: list[RecipeIngredientItem] = []

    recipe_groups = list(RecipeIngredientItemGroup.objects.filter(recipe_id=recipe_id))
    existing_recipe_ingredient_items = list(
        RecipeIngredientItem.objects.filter(ingredient_group__recipe_id=recipe_id)
    )

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
        logger.info("Creating ingredient items", amount=len(ingredient_items_to_create))
        RecipeIngredientItem.objects.bulk_create(ingredient_items_to_create)

    if len(ingredient_items_to_update):
        logger.info(
            "Updating ingredient items",
            items=[item.id for item in ingredient_items_to_update],
        )
        RecipeIngredientItem.objects.bulk_update(
            ingredient_items_to_update,
            fields=[
                "ingredient_group_id",
                "ingredient_id",
                "portion_quantity",
                "portion_quantity_unit_id",
            ],
        )

    ingreident_items_ids_to_delete = [
        ingredient_item.id
        for ingredient_item in existing_recipe_ingredient_items
        if ingredient_item.id not in [item.id for item in ingredient_items_to_update]
    ]

    if len(ingreident_items_ids_to_delete):
        logger.info("Deleting ingredient items", items=ingreident_items_ids_to_delete)
        RecipeIngredientItem.objects.filter(
            id__in=ingreident_items_ids_to_delete
        ).delete()


def _validate_ingredient_item_groups(
    ingredient_group_items: list[IngredientGroupItem]
) -> None:
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
def create_or_update_recipe_ingredient_item_groups(
    recipe_id: int,
    ingredient_item_groups: list[IngredientGroupItem],
) -> None:
    if not ingredient_item_groups:
        return None

    _validate_ingredient_item_groups(ingredient_group_items=ingredient_item_groups)

    existing_groups = list(
        RecipeIngredientItemGroup.objects.filter(recipe_id=recipe_id)
    )

    groups_to_create: list[RecipeIngredientItemGroup] = []
    groups_to_update: list[RecipeIngredientItemGroup] = []

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

    if len(groups_to_create):
        RecipeIngredientItemGroup.objects.bulk_create(groups_to_create)

    if len(groups_to_update):
        RecipeIngredientItemGroup.objects.bulk_update(
            groups_to_update,
            fields=["title", "ordering"],
        )

    group_ids_to_delete = [
        group.id
        for group in existing_groups
        if group.id not in [item_group.id for item_group in groups_to_update]
    ]

    if len(group_ids_to_delete):
        RecipeIngredientItemGroup.objects.filter(id__in=group_ids_to_delete).delete()

    transaction.on_commit(
        functools.partial(
            create_or_update_recipe_ingredient_items,
            recipe_id=recipe_id,
            groups=ingredient_item_groups,
        )
    )
