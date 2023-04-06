# Generated by Django 4.1.7 on 2023-03-28 13:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nest", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Home",
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
                ("street_address", models.CharField(max_length=255)),
                ("zip_code", models.CharField(max_length=10)),
                ("zip_place", models.CharField(max_length=50)),
                ("num_residents", models.BigIntegerField()),
                ("num_weeks_recipe_rotation", models.BigIntegerField(default=2)),
                ("weekly_budget", models.DecimalField(decimal_places=2, max_digits=10)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "home",
                "verbose_name_plural": "homes",
            },
        ),
        migrations.AddField(
            model_name="user",
            name="home",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="residents",
                to="nest.home",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="homes",
            field=models.ManyToManyField(
                blank=True, related_name="users", to="nest.home"
            ),
        ),
    ]
