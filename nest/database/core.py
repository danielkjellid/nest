from nest import config
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(config.DATABASE_URL, echo=True, future=True)
