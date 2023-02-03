import asyncio

import pytest
import pytest_asyncio
from sqlalchemy import event
from httpx import AsyncClient
from nest.app import app
from sqlalchemy.ext.asyncio.session import AsyncSession
from nest.database.sessions import AsyncDatabaseSession

import sqlalchemy
from nest import config
from typing import Generator


class DBStatementCounter(object):
    """
    Use as a context manager to count the number of execute()'s performed
    against the given sqlalchemy connection.

    Usage:
        with DBStatementCounter(conn) as ctr:
            conn.execute("SELECT 1")
            conn.execute("SELECT 1")
        assert ctr.get_count() == 2
    """

    def __init__(self, conn):
        self.conn = conn
        self.count = 0
        # Will have to rely on this since sqlalchemy 0.8 does not support
        # removing event listeners
        self.do_count = False
        sqlalchemy.event.listen(conn, "after_execute", self.callback)

    def __enter__(self):
        self.do_count = True
        return self

    def __exit__(self, *_):
        self.do_count = False

    def get_count(self):
        return self.count

    def callback(self, *_):
        if self.do_count:
            self.count += 1


# class CaptureQueriesContext(object):
#     """
#     Context manager that captures queries executed by a specific connection.
#     """
#
#     def __init__(self, connection):
#         self.connection = connection
#         event.listen(self.connection, "after_execute", self.callback)
#
#     def __iter__(self):
#         return iter(self.captured_queries)
#
#     def __getitem__(self, index):
#         return self.captured_queries[index]
#
#     def __len__(self):
#         return len(self.captured_queries)
#
#     @property
#     def captured_queries(self):
#         self.connection.queries[self.initial_queries : self.final_queries]
#
#     def __enter__(self):
#         self.force_debug_cursor = self.connection.force_debug_cursor
#         self.connection.force_debug_cursor = True
#
#         self.connection.ensure_connection()
#         self.initial_queries = len(self.connection.queries_log)
#         self.final_queries = None
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.connection.force_debug_cursor = self.force_debug_cursor
#         if exc_type is not None:
#             return
#         self.final_queries = len(self.connection.queries_log)
#         event.remove(self.connection, "before_cursor_execute", self.callback)


def _assert_num_queries(
    config, num: int, exact: bool = True, connection=None, info=None
):
    pass


@pytest.fixture(autouse=True)
def set_test_db():
    config.DATABASE_URL = "postgresql+asyncpg://nest:nest@localhost:5433/nest_test"


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=app, base_url="/") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncSession:
    session = AsyncDatabaseSession()
    session.init()
    session.create_all()

    yield session

    session.dispose()
