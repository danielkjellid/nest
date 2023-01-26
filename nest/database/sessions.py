from uuid import uuid4

from nest import config
from nest.database.utils import (
    get_session_context,
    reset_session_context,
    set_session_context,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kwargs):
        return create_async_engine(config.DATABASE_URL, pool_recycle=3600).sync_engine


async_session_factory = sessionmaker(
    class_=AsyncSession, sync_session_class=RoutingSession
)

session: AsyncSession | async_scoped_session = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)


def offline_session(func):
    """
    We set the normal sesssion through a middleware, however, it does not
    go through middleware in tests or background tasks, so an offline
    session is needed to provision access to the database.

    Example:
        from nest.database import offline_session

       @offline_session
       def test_something():
            ...
    """

    async def _offline_session(*args, **kwargs):
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
