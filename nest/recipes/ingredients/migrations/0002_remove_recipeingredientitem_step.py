# Generated by Django 4.2.7 on 2024-06-18 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes_ingredients', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeingredientitem',
            name='step',
        ),
    ]