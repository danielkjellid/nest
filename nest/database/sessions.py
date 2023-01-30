from typing import Any, Callable
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker

from nest.database.base import Base
from nest.database.core import engine
from nest.database.utils import (
    get_session_context,
    reset_session_context,
    set_session_context,
)

async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

session = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name: str):
        return getattr(self._session, name)

    def init(self):
        self._engine = engine
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


db = AsyncDatabaseSession()


def offline_session(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    We set the normal session through a middleware, however, it does not
    go through middleware in tests or background tasks, so an offline
    session is needed to provision access to the database.

    Example:
        from nest.database import offline_session

       @offline_session
       def test_something():
            ...
    """

    async def _offline_session(*args: Any, **kwargs: Any) -> None:
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            await func(*args, **kwargs)
        except Exception as exc:
            await session.rollback()
            raise exc
        finally:
            await session.remove()
            reset_session_context(context=context)

    return _offline_session
