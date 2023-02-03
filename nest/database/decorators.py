from functools import wraps
from typing import Any, Callable, TypeVar
from typing_extensions import ParamSpec

from nest.database.sessions import session

P = ParamSpec("P")
R = TypeVar("R")


def transaction(func: Callable[P, R]) -> Callable[P, R]:
    """
    Run an async query in a transaction, rolling back on raised exceptions.

    Example:
        from nest.database import transaction, session

        @transaction
        async def create_user(self)
             session.add(User(email="user@example.com"))
    """

    async def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            result = await func(*args, **kwargs)
            await session.commit()
        except Exception as exc:
            await session.rollback()
            raise exc

        return result

    return inner
