from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from nest import config
from nest.api.v1 import v1_router
from nest.middlewares import LoggingMiddleware
from nest.database import session


def init_routers(app_: FastAPI) -> None:
    app_.include_router(v1_router)


def init_middlewares() -> list[Middleware]:
    middlewares = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(LoggingMiddleware),
        Middleware(CorrelationIdMiddleware),
    ]

    return middlewares


def create_app() -> FastAPI:
    session.init()

    app_ = FastAPI(
        title="Nest",
        description="Nest API",
        version="1.0.0",
        docs_url=None if config.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if config.ENVIRONMENT == "production" else "/redoc",
        middleware=init_middlewares(),
    )
    init_routers(app_=app_)

    return app_


app = create_app()


@app.on_event("startup")
async def startup():
    await session.create_all()


@app.on_event("shutdown")
async def shutdown():
    await session.close()
