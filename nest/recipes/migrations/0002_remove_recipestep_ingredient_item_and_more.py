# Generated by Django 4.1.7 on 2023-08-15 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recipestep",
            name="ingredient_item",
        ),
        migrations.AddField(
            model_name="recipeingredientitem",
            name="step",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="ingredient_items",
                to="recipes.recipestep",
            ),
        ),
    ]