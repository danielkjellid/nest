from pathlib import Path

import structlog
from django.apps import AppConfig
from django.conf import settings
from django.core.management import call_command

logger = structlog.getLogger()


class ApisConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nest.api"

    # def ready(self) -> None:
    #     if not getattr(settings, "OPENAPI_AUTO_GENERATE", False):
    #         return
    #
    #     openapi_schema_path_setting = getattr(settings, "OPENAPI_SCHEMA_PATH", None)
    #     base_path = settings.BASE_DIR
    #
    #     if not openapi_schema_path_setting:
    #         folder_path = base_path.resolve()
    #     else:
    #         folder_path = base_path / Path(openapi_schema_path_setting).resolve()
    #
    #     # Make sure folder exist.
    #     folder_path.mkdir(parents=True, exist_ok=True)
    #     path = folder_path / "schema.json"
    #
    #     with open(path, "w", encoding="utf-8"):
    #         call_command("export_schema", output=path)
    #         logger.info("Wrote API OpenAPI schema to %s", path)
