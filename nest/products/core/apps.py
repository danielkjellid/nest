from django.apps import AppConfig


class ProductsCoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nest.products.core"
    label = "products"

    def ready(self) -> None:
        import nest.products.core.signals  # noqa
