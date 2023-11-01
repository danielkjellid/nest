from ninja import Router

from .core.endpoints import router as core_router

users_router = Router(tags=["Users"])

users_router.add_router(prefix="", router=core_router)
