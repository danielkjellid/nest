from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime

from nest.database import Base


class BaseSchema(Base):
    """
    Base schema storing the most important fields to be used in other models.
    """

    __abstract__ = True

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        index=True,
        nullable=False,
        unique=True,
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.utcnow)
