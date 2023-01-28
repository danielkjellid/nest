from nest.database import Base
from nest.models.base import BaseSchema
from pydantic import BaseModel
from sqlalchemy import BigInteger, Column, String


class UserModel(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    full_name: str


class UserSchema(BaseSchema):
    email = Column(String, nullable=False, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
