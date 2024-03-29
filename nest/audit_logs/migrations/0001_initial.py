# Generated by Django 4.1.7 on 2023-05-01 19:25

import django.core.serializers.json
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LogEntry",
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
                ("object_repr", models.TextField()),
                (
                    "object_id",
                    models.BigIntegerField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="log object id",
                    ),
                ),
                (
                    "action",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "create"), (1, "update"), (2, "delete")],
                        verbose_name="action",
                    ),
                ),
                (
                    "changes",
                    models.JSONField(
                        blank=True,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                        null=True,
                    ),
                ),
                ("remote_addr", models.GenericIPAddressField(blank=True, null=True)),
                ("source", models.TextField(blank=True, null=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="contenttypes.contenttype",
                        verbose_name="log content type",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "log entry",
                "verbose_name_plural": "log entries",
                "ordering": ["-created_at"],
                "get_latest_by": "created_at",
            },
        ),
    ]
