from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nest.users"

    def ready(self) -> None:
        import nest.users.signals  # noqa
