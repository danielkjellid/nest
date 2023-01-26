from fastapi import APIRouter

# from .users import user_router
from .users import users_router

# def init_v1_routers(router: APIRouter) -> list[APIRouter]:
#     return [user_router]
#     # router.include_router(user_router, prefix="/users", tags=["Users"])


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(users_router, prefix="/users", tags=["Users"])

__all__ = ["v1_router"]
