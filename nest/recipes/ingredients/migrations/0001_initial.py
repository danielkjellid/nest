# Generated by Django 4.1.7 on 2023-10-30 15:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("recipes_steps", "0001_initial"),
        ("recipes", "0001_initial"),
        ("products", "0003_product_allergens_product_carbohydrates_and_more"),
        ("units", "0002_auto_20230413_1530"),
    ]

    operations = [
        migrations.CreateModel(
            name="RecipeIngredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="created time"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="modified time"),
                ),
                ("title", models.CharField(max_length=255, unique=True)),
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ingredient",
                        to="products.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "ingredient",
                "verbose_name_plural": "ingredients",
            },
        ),
        migrations.CreateModel(
            name="RecipeIngredientItemGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="created time"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="modified time"),
                ),
                ("title", models.CharField(max_length=255)),
                ("ordering", models.PositiveIntegerField()),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ingredient_groups",
                        to="recipes.recipe",
                    ),
                ),
            ],
            options={
                "verbose_name": "ingredient group",
                "verbose_name_plural": "ingredient groups",
            },
        ),
        migrations.CreateModel(
            name="RecipeIngredientItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="created time"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="modified time"),
                ),
                (
                    "additional_info",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "portion_quantity",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ingredient_items",
                        to="recipes_ingredients.recipeingredient",
                    ),
                ),
                (
                    "ingredient_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ingredient_items",
                        to="recipes_ingredients.recipeingredientitemgroup",
                    ),
                ),
                (
                    "portion_quantity_unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="units.unit",
                    ),
                ),
                (
                    "step",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="ingredient_items",
                        to="recipes_steps.recipestep",
                    ),
                ),
            ],
            options={
                "verbose_name": "ingredient item",
                "verbose_name_plural": "ingredient items",
            },
        ),
    ]
