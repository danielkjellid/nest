from django.apps import AppConfig


class UsersCoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nest.users.core"

    def ready(self) -> None:
        import nest.users.core.signals  # noqa

    label = "users"
