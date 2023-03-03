from pydantic import BaseModel
from typing import Literal


class JWTPairRecord(BaseModel):
    access_token: str
    refresh_token: str


class TokenBaseRecord(BaseModel):
    iat: int
    iss: str
    user_id: int


class TokenRecord(TokenBaseRecord):
    token_type: Literal["access", "refresh"]
    exp: int
    jti: str
