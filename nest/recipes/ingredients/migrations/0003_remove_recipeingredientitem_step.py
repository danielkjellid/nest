# Generated by Django 4.2.7 on 2024-06-19 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes_ingredients', '0002_alter_recipeingredient_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeingredientitem',
            name='step',
        ),
    ]