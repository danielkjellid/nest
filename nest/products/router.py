from ninja import Router

from .core.endpoints import router as core_router
from .oda.endpoints import router as oda_router

products_router = Router(tags=["Products"])

products_router.add_router(prefix="", router=core_router)
products_router.add_router(prefix="oda", router=oda_router)
