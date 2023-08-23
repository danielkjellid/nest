# Generated by Django 4.1.7 on 2023-08-23 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0003_product_allergens_product_carbohydrates_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ingredient",
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
    ]
