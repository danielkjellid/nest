# Generated by Django 4.1.7 on 2023-08-22 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_product_allergens_product_carbohydrates_and_more"),
        ("ingredients", "0003_alter_ingredient_product_alter_ingredient_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="product",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient",
                to="products.product",
            ),
        ),
    ]
