from nest import config
from nest.database.base import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine(config.DATABASE_URL, echo=True, future=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
