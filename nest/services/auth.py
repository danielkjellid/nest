from datetime import datetime
from nest.records import TokenRecord, JWTPairRecord, TokenBaseRecord
from nest import config
from uuid import uuid4
import jwt
from nest.database import session
from sqlalchemy import select

from nest.models import OutstandingToken, User, BlacklistedToken
from nest.selectors import AuthSelector

ISSUER = config.NEST_JWT_ISSUER
SIGNING_KEY = config.NEST_JWT_SECRET_KEY
ACCESS_KEY_LIFESPAN = config.NEST_JWT_ACCESS_EXP
REFRESH_KEY_LIFESPAN = config.NEST_JWT_REFRESH_EXP
ALGORITHM = config.NEST_JWT_ALG


class AuthService:
    def __init__(self):
        ...

    @staticmethod
    def _access_token_create_and_encode(payload: TokenBaseRecord) -> str:
        """
        Encode an access token.
        """

        access_to_expire_at = datetime.utcnow() + ACCESS_KEY_LIFESPAN

        token_payload = TokenRecord(
            token_type="access",
            exp=access_to_expire_at,
            jti=uuid4().hex,
            **payload.dict(),
        )

        encoded_access_token = jwt.encode(
            token_payload.dict(), SIGNING_KEY, algorithm=ALGORITHM
        )

        return encoded_access_token

    @staticmethod
    async def _refresh_token_create_and_encode(payload: TokenBaseRecord) -> str:
        """
        Encode a refresh token, and store properties in the database.
        """

        refresh_to_expire_at = datetime.utcnow() + REFRESH_KEY_LIFESPAN

        token_payload = TokenRecord(
            token_type="refresh",
            exp=refresh_to_expire_at,
            jti=uuid4().hex,
            **payload.dict(),
        )

        encoded_refresh_token = jwt.encode(
            token_payload.dict(), SIGNING_KEY, algorithm=ALGORITHM
        )

        outstanding_token = OutstandingToken(
            user_id=token_payload.user_id,
            jti=token_payload.jti,
            token=encoded_refresh_token,
            created_at=token_payload.iat,
            expires_at=token_payload.exp,
        )

        session.add(outstanding_token)
        await session.commit().commit()

        return encoded_refresh_token

    @classmethod
    def token_pair_for_user(cls, user_id: int) -> JWTPairRecord:
        """
        Create a token pair of both access and refresh token for a user.
        """

        payload = TokenBaseRecord(iat=datetime.utcnow(), iss=ISSUER, user_id=user_id)

        encoded_access_token = cls._access_token_create_and_encode(payload=payload)
        encoded_refresh_token = cls._refresh_token_create_and_encode(payload=payload)

        return JWTPairRecord(
            access_token=encoded_access_token, refresh_token=encoded_refresh_token
        )

    @classmethod
    async def token_pair_from_refresh_token(cls, token: str) -> JWTPairRecord:
        """
        Create a new token pair based on valid refresh token.
        """

        is_valid, decoded_token = AuthSelector.is_refresh_token_valid(
            refresh_token=token
        )

        if not is_valid:
            raise ValueError("Refresh token provided is invalid.")

        if decoded_token is None:
            raise ValueError("Decoded token is invalid.")

        user = await session.get(User, decoded_token.user_id)

        if not user:
            raise ValueError("Issued user in refresh token does not exist.")

        return cls.token_pair_for_user(user_id=user.id)

    @classmethod
    async def blacklist_refresh_token(cls, refresh_token: str) -> None:
        """
        Adds a refresh token to list over blacklisted tokens, invalidating it.
        """

        is_valid, decoded_token = AuthSelector.is_refresh_token_valid(
            refresh_token=refresh_token
        )

        if not is_valid:
            raise ValueError("Refresh token provided is invalid.")

        if decoded_token is None:
            raise ValueError("Decoded token is invalid.")

        token_instance = await session.get(
            OutstandingToken, jti=decoded_token.jti, user_id=decoded_token.user_id
        )

        if not token_instance:
            raise ValueError("Refresh token provided does not exist.")

        session.add(BlacklistedToken(token_id=token_instance.id))
        session.commit()
