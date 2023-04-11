from .users import router as users_endpoints
from .products import router as products_endpoints

__all__ = ["products_endpoints", "users_endpoints"]
