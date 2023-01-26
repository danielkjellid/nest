from nest.database import Base
from sqlalchemy import BigInteger, Column, String


class User(Base):
    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        index=True,
        nullable=False,
        unique=True,
    )
    first_name = Column(String)
    last_name = Column(String)
