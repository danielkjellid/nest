from decimal import Decimal
from typing import Any

from django.db import transaction
from django.http import HttpRequest

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


def create_recipe_ingredient_item_groups(
    *, recipe_id: int | str, ingredient_group_items: list[dict[str, Any]]
) -> None:
    """
    Create ingredient item groups and related ingredient items and associate them with a
    recipe.
    """

    # Sanity check that we only are dealing with unique ordering properties.
    ordering = [group["ordering"] for group in ingredient_group_items]
    if not len(set(ordering)) == len(ordering):
        raise ApplicationError(
            message="Ordering for ingredient group items has to be unique"
        )

    # Sanity check that we are only dealing with unique instructions.
    titles = [group["title"] for group in ingredient_group_items]
    if not len(set(titles)) == len(titles):
        raise ApplicationError(
            message="Titles for ingredient group items has to be unique"
        )

    # Create a list of which ingredient_group_items to bulk create.
    recipe_ingredient_groups_to_create = [
        RecipeIngredientItemGroup(
            recipe_id=recipe_id,
            title=item_group["title"],
            ordering=item_group["ordering"],
        )
        for item_group in ingredient_group_items
    ]

    # Do all transactions atomically so that we can take advantage of the on_commit
    # callback.
    with transaction.atomic():
        # Create ingredient_item_groups.
        created_ingredient_item_groups = RecipeIngredientItemGroup.objects.bulk_create(
            recipe_ingredient_groups_to_create
        )

        try:
            ingredient_items_to_create = [
                RecipeIngredientItem(
                    # Try to find associated group though generator, as created_
                    # ingredient_item_groups should return a list of created objects.
                    ingredient_group_id=next(
                        group.id
                        for group in created_ingredient_item_groups
                        if group.title == item_group["title"]
                        and group.ordering == item_group["ordering"]
                    ),
                    ingredient_id=ingredient_item["ingredient_id"],
                    additional_info=(
                        ingredient_item["additional_info"]
                        if ingredient_item["additional_info"]
                        else None
                    ),
                    portion_quantity=Decimal(ingredient_item["portion_quantity"]),
                    portion_quantity_unit_id=int(
                        ingredient_item["portion_quantity_unit_id"]
                    ),
                )
                for item_group in ingredient_group_items
                for ingredient_item in item_group["ingredient_items"]
            ]
        except StopIteration as exc:
            raise ApplicationError(
                message="Could not find group to connect to ingredient item."
            ) from exc

        def create_ingredient_items() -> None:
            RecipeIngredientItem.objects.bulk_create(ingredient_items_to_create)

        # Once groups has been created, use callback to create associated
        # ingredient_items.
        transaction.on_commit(create_ingredient_items)
