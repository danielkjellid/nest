from ninja import Router

from .core.endpoints import router as core_router
from .ingredients.endpoints import router as ingredients_router
from .steps.endpoints import router as steps_router

recipes_router = Router(tags=["Recipes"])

recipes_router.add_router(prefix="", router=core_router)
recipes_router.add_router(prefix="ingredients", router=ingredients_router)
recipes_router.add_router(prefix="steps", router=steps_router)
