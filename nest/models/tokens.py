from pydantic import BaseModel
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from nest.models import User
from datetime import datetime
from nest.database import Base, PrimaryKeyMixin


class OutstandingTokenSchema(BaseModel):
    id: int
    user_id: int
    jti: str
    token: str
    created_at: datetime
    expires_at: datetime

    class Config:
        orm_mode = True


class OutstandingToken(Base, PrimaryKeyMixin):
    """
    A JWT refresh token.
    """

    user_id = Column(
        Integer, ForeignKey("users_user.id", ondelete="SET NULL"), nullable=True
    )
    jti = Column(String, unique=True)
    token = Column(String)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    expires_at = Column(DateTime)

    user = relationship(User, backref="tokens")

    def __repr__(self) -> str:
        return f"Token for {self.user} ({self.jti})"


class BlacklistedTokenSchema(BaseModel):
    blacklisted_at: datetime
    token_id: int

    class Config:
        orm_mode = True


class BlacklistedToken(Base, PrimaryKeyMixin):
    """
    A blacklisted refresh token.
    """

    blacklisted_at = Column(DateTime, default=datetime.utcnow)
    token_id = Column(
        Integer,
        ForeignKey("tokens_outstanding_token.id", ondelete="CASCADE"),
        nullable=False,
    )

    token = relationship(OutstandingToken, backref="blacklisted_token", uselist=False)

    def __repr__(self) -> str:
        return f"Blacklisted token for {self.token.user}"
