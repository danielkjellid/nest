from sqlalchemy.ext.asyncio.session import AsyncSession
from nest.database import session as db_session


class BaseService:
    def __init__(self, session: AsyncSession | None = None) -> None:
        self.session = session if session else db_session
