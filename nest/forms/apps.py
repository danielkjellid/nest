from django.apps import AppConfig
from django.conf import settings
from django.core.management import call_command
import structlog
from pathlib import Path

logger = structlog.getLogger()


class FormsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nest.forms"

    def ready(self) -> None:
        if not getattr(settings, "FORMS_AUTO_GENERATE", False):
            return

        forms_schema_path_setting = getattr(settings, "FORMS_SCHEMA_PATH", None)
        base_path = settings.BASE_DIR

        if not forms_schema_path_setting:
            folder_path = base_path.resolve()
        else:
            folder_path = base_path / Path(forms_schema_path_setting).resolve()

        # Make sure folder exist.
        folder_path.mkdir(parents=True, exist_ok=True)
        path = folder_path / "forms.json"

        with open(path, "w", encoding="utf-8"):
            call_command("export_forms", output=path)
            logger.info("Wrote Forms OpenAPI schema to %s", path)
