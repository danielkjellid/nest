from .product_create import *  # noqa
from .product_detail import *  # noqa
from .product_edit import *  # noqa
from .product_list import *  # noqa
from .product_oda_import import *  # noqa
from .product_oda_import_confirm import *  # noqa

from .router import router as products_router

__all__ = ["products_router"]
