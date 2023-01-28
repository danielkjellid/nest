from sqlalchemy.ext.asyncio import create_async_engine

from nest import config

engine = create_async_engine(config.DATABASE_URL, echo=True, future=True)
