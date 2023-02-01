from pydantic import BaseModel
from sqlalchemy import Column, String, Integer
from nest.database import TimestampMixin, Base, PrimaryKeyMixin


class UserSchema(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    full_name: str

    class Config:
        orm_mode = True


class User(Base, TimestampMixin, PrimaryKeyMixin):
    email = Column(String, nullable=False, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
