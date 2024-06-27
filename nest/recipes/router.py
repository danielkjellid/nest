from ninja import Router

from .core.endpoints import router as core_router
from .ingredients.endpoints import router as ingredients_router
from .plans.endpoints import router as plans_router

recipes_router = Router(tags=["Recipes"])

recipes_router.add_router(prefix="", router=core_router)
recipes_router.add_router(prefix="ingredients", router=ingredients_router)
recipes_router.add_router(prefix="plans", router=plans_router)
