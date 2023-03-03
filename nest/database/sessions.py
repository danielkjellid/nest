from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from alembic import command as alembic_command, script
from alembic.config import Config as AlembicConfig
from alembic.runtime import migration
from nest import config

from .base import Base


class AsyncDatabaseSession:
    def __init__(self, db_url: str | None = None) -> None:
        self.db_url = db_url if db_url else config.DATABASE_URL
        self._engine: AsyncEngine = None
        self._session: AsyncSession = None

    def __getattr__(self, name: str) -> None:
        return getattr(self._session, name)

    def init(self) -> None:
        self._engine: AsyncEngine = create_async_engine(
            self.db_url, echo=config.LOG_SQLALCHEMY, future=True
        )

        self._session: AsyncSession = sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )()

    async def create_all(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def dispose(self) -> None:
        await self.drop_all()
        self.close()
        self._engine.dispose()

    async def apply_revisions(self) -> None:
        alembic_cfg = AlembicConfig(config.ALEMBIC_INI_PATH)
        alembic_cfg.set_main_option("sqlalchemy.url", self.db_url)
        script_ = script.ScriptDirectory.from_config(alembic_cfg)

        async with self._engine.begin() as conn:
            # context = migration.MigrationContext.configure(conn)
            # current_revision = await context.get_current_revision()
            # print("hits here")
            #
            # if current_revision == script_.get_current_head():
            #     print("hit here")
            #     return
            # print("here instead")
            print("hits here")
            alembic_command.upgrade(alembic_cfg, "head")
            print("hits here instead")


session = AsyncDatabaseSession()
