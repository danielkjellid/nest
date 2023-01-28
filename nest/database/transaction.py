from functools import wraps
from typing import Any, Callable

from nest.database.sessions import session


class Transactional:
    """
    Run an async query in a transaction, rolling back on raised exceptions.

    Example:
        from nest.database import Transactional, session

        @Transactional()
        async def create_user(self)
             session.add(User(email="user@example.com"))
    """

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def _transactional(*args: Any, **kwargs: Any) -> Any:
            try:
                result = await func(*args, **kwargs)
                await session.commit()
            except Exception as exc:
                await session.rollback()
                raise exc

            return result

        return _transactional
