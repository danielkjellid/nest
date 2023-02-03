from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
)
from sqlalchemy.orm import sessionmaker

from nest.database.core import engine
from .base import Base

async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class AsyncDatabaseSession:
    def __init__(self) -> None:
        self._engine: AsyncEngine = None
        self._session: AsyncSession = None

    def __getattr__(self, name: str) -> None:
        return getattr(self._session, name)

    def init(self):
        self._engine: AsyncEngine = engine
        self._session: AsyncSession = sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def dispose(self):
        await self.drop_all()
        self.close()
        self._engine.dispose()


session = AsyncDatabaseSession()
