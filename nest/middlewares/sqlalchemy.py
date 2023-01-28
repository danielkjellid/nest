from uuid import uuid4

from starlette.types import ASGIApp, Receive, Scope, Send

from nest.database import session
from nest.database.utils import reset_session_context, set_session_context


class SQLAlchemyMiddleware:
    """
    Middle to initialize async database session.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            raise exc
        finally:
            await session.remove()
            reset_session_context(context=context)
