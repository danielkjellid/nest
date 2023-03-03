import jwt
from nest.records import TokenRecord, TokenBaseRecord, JWTPairRecord
from django.conf import settings
from uuid import uuid4
from nest.models import OutstandingToken, BlacklistedToken, User
from django.utils import timezone
from nest.selectors import AuthSelector
from nest.exceptions import ApplicationError

ACCESS_KEY_LIFESPAN = settings.NEST_JWT_ACCESS_TOKEN_EXP
REFRESH_KEY_LIFESPAN = settings.NEST_JWT_REFRESH_TOKEN_EXP
SIGNING_KEY = settings.NEST_JWT_SIGNING_KEY
ALGORITHM = settings.NEST_JWT_ALG
ISSUER = settings.NEST_JWT_ISSUER


class AuthService:
    def __init__(self):
        ...

    @classmethod
    def token_pair_for_user(cls, user_id: int) -> JWTPairRecord:
        """
        Create a token pair of both access and refresh token for a user.
        """

        payload = TokenBaseRecord(iat=timezone.now(), iss=ISSUER, user_id=user_id)

        encoded_access_token = cls._access_token_create_and_encode(payload=payload)
        encoded_refresh_token = cls._refresh_token_create_and_encode(payload=payload)

        return JWTPairRecord(
            access_token=encoded_access_token, refresh_token=encoded_refresh_token
        )

    @classmethod
    def token_pair_from_refresh_token(cls, token: str) -> JWTPairRecord:
        """
        Create a new token pair based on valid refresh token.
        """

        is_valid, decoded_token = AuthSelector.is_refresh_token_valid(
            refresh_token=token
        )

        if not is_valid:
            raise ApplicationError("Refresh token provided is invalid.")

        if decoded_token is None:
            raise ApplicationError("Decoded token is invalid.")

        user = User.objects.get(decoded_token.user_id)

        if not user:
            raise ApplicationError("Issued user in refresh token does not exist.")

        return cls.token_pair_for_user(user_id=user.id)

    @classmethod
    def blacklist_refresh_token(cls, refresh_token: str) -> None:
        """
        Adds a refresh token to list over blacklisted tokens, invalidating it.
        """

        is_valid, decoded_token = AuthSelector.is_refresh_token_valid(
            refresh_token=refresh_token
        )

        if not is_valid:
            raise ApplicationError("Refresh token provided is invalid.")

        if decoded_token is None:
            raise ApplicationError("Decoded token is invalid.")

        token_instance = OutstandingToken.objects.filter(
            jti=decoded_token.jti, user_id=decoded_token.user_id
        ).first()

        if not token_instance:
            raise ApplicationError("Refresh token provided does not exist.")

        BlacklistedToken.objects.create(token=token_instance)

    @staticmethod
    def _access_token_create_and_encode(payload: TokenBaseRecord) -> str:
        """
        Encode an access token.
        """

        access_to_expire_at = timezone.now() + ACCESS_KEY_LIFESPAN

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
    def _refresh_token_create_and_encode(payload: TokenBaseRecord) -> str:
        """
        Encode a refresh token, and store properties in the database.
        """

        refresh_to_expire_at = timezone.now() + REFRESH_KEY_LIFESPAN

        token_payload = TokenRecord(
            token_type="refresh",
            exp=refresh_to_expire_at,
            jti=uuid4().hex,
            **payload.dict(),
        )

        encoded_refresh_token = jwt.encode(
            token_payload.dict(), SIGNING_KEY, algorithm=ALGORITHM
        )

        OutstandingToken.objects.create(
            user_id=token_payload.user_id,
            jti=token_payload.jti,
            token=encoded_refresh_token,
            created_at=token_payload.iat,
            expires_at=token_payload.exp,
        )

        return encoded_refresh_token
