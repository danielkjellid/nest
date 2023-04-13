from .products import router as products_endpoints
from .users import router as users_endpoints

__all__ = ["products_endpoints", "users_endpoints"]
