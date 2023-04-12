# Generated by Django 4.1.7 on 2023-04-12 09:39

from django.db import migrations, models
import django.db.models.deletion
import nest.models.products


class Migration(migrations.Migration):

    dependencies = [
        ("nest", "0004_auto_20230411_1739"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=255)),
                ("gross_price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "gross_unit_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "unit_quantity",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("oda_url", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "oda_id",
                    models.PositiveBigIntegerField(blank=True, null=True, unique=True),
                ),
                ("is_available", models.BooleanField(default=True)),
                (
                    "thumbnail",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=nest.models.products.Product.get_product_upload_path,
                    ),
                ),
                ("gtin", models.CharField(blank=True, max_length=14, null=True)),
                ("supplier", models.CharField(max_length=50)),
                (
                    "is_synced",
                    models.BooleanField(
                        default=True, help_text="Product is kept in sync from Oda."
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="products",
                        to="nest.unit",
                    ),
                ),
            ],
            options={
                "verbose_name": "product",
                "verbose_name_plural": "products",
            },
        ),
    ]
