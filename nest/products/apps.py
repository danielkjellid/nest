from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nest.products"

    def ready(self) -> None:
        import nest.products.signals  # noqa
