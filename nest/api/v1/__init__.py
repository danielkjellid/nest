from fastapi import APIRouter
from nest.api.v1.users import user_router

v1_router = APIRouter(prefix="v1/")
v1_router.include_router(user_router, prefix="users/", tags=["Users"])


__all__ = ["v1_router"]
