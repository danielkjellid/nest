from nest.records import TokenRecord, TokenBaseRecord, JWTPairRecord
import jwt
from django.conf import settings
from nest.exceptions import ApplicationError
from nest.models import OutstandingToken, BlacklistedToken

ACCESS_KEY_LIFESPAN = settings.NEST_JWT_ACCESS_TOKEN_EXP
REFRESH_KEY_LIFESPAN = settings.NEST_JWT_REFRESH_TOKEN_EXP
SIGNING_KEY = settings.NEST_JWT_SIGNING_KEY
ALGORITHM = settings.NEST_JWT_ALG
ISSUER = settings.NEST_JWT_ISSUER


class AuthSelector:
    def __init__(self):
        ...

    @classmethod
    def is_refresh_token_valid(
        cls, refresh_token: str
    ) -> tuple[bool, TokenRecord | None]:
        """
        Verify validity of a given refresh token. Checks token expiry, type and if it's
        blacklisted. Also checks if it's issues to the correct user and if we're able
        to decode it with our signing key.
        """

        try:
            # This throw an exception is we're unable to decode the
            # provided token, we can therefore assume that all token
            # data beyond this point is decoded.
            decoded_token = cls._decode_token(token=refresh_token)

            token_type = decoded_token.token_type
            token_jti = decoded_token.jti
            token_user_id = decoded_token.user_id

            # Check that we're validating a refresh token type.
            if token_type != "refresh":
                return False, None  # Unexpected token type.

            # Check that token belongs to user and is not already blacklisted.
            outstanding_token = OutstandingToken.objects.filter(
                jti=token_jti, user_id=token_user_id
            )

            if not outstanding_token.exists():
                return False, None  # Provided Token does not belong to issued user.

            if outstanding_token.first().blacklisted_token is not None:
                return False, None  # Token is already blacklisted.

            # If we've successfully decoded token and passed all the checks above,
            # the token is valid.
            return True, decoded_token
        except jwt.ExpiredSignatureError:
            return False, None  # Token has expired.
        except Exception as exc:  # noqa
            return False, None  # Something else went wrong, unable to validate.

    @classmethod
    def is_access_token_valid(
        cls, access_token: str
    ) -> tuple[bool, TokenRecord | None]:
        """
        Verify the validity of a given access token. Checks token expiry, type and if
        we're able to decode it.
        """

        try:
            decoded_token = cls._decode_token(token=access_token)
            token_type = decoded_token.token_type

            # Check that we're validating a refresh token type.
            if token_type != "access":
                return False, None  # Unexpected token type.

            # If we've successfully decoded token and passed all the checks above,
            # the token is valid.
            return True, decoded_token
        except jwt.ExpiredSignatureError:
            return False, None  # Token has expired.
        except Exception as exc:  # noqa
            return False, None  # Something else went wrong, unable to validate

    @staticmethod
    def _decode_token(token: str) -> TokenRecord:
        """
        The most basic decoding and validation. Decodes token, checking
        signature and expiration. Use the is_refresh_token_valid instead as additional
        checks should be made alongside.
        """

        try:
            decoded_token = jwt.decode(
                token, SIGNING_KEY, algorithms=[ALGORITHM], issuer=ISSUER
            )

            return TokenRecord(
                token_type=decoded_token["token_type"],
                exp=decoded_token["exp"],
                iat=decoded_token["iat"],
                jti=decoded_token["jti"],
                iss=decoded_token["iss"],
                user_id=decoded_token["user_id"],
            )
        # Checking token expiry may lead to an exception, we want to explicitly
        # handle it by returning False instead in our is_valid selectors.
        except jwt.ExpiredSignatureError as jwt_exc:
            raise jwt_exc
        except Exception as exc:
            raise ApplicationError(f"Unable to decode provided token: {exc}") from exc
