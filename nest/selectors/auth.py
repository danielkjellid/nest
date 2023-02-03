import jwt
from nest.records import TokenRecord
from nest import config
from sqlalchemy import select, and_
from nest.models import OutstandingToken
from nest.database import session

ISSUER = config.NEST_JWT_ISSUER
SIGNING_KEY = config.NEST_JWT_SECRET_KEY
ACCESS_KEY_LIFESPAN = config.NEST_JWT_ACCESS_EXP
REFRESH_KEY_LIFESPAN = config.NEST_JWT_REFRESH_EXP
ALGORITHM = config.NEST_JWT_ALG


class AuthSelector:
    def __init__(self):
        ...

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
            raise ValueError(f"Unable to decode provided token: {exc}") from exc

    @classmethod
    async def is_refresh_token_valid(
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
            query = await session.execute(
                select(OutstandingToken).where(
                    and_(
                        OutstandingToken.jti == token_jti,
                        OutstandingToken.user_id == token_user_id,
                    )
                )
            )
            outstanding_token = query.scalars().first()

            if not outstanding_token:
                return False, None  # Provided Token does not belong to issued user.

            if outstanding_token.blacklisted_token is not None:
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
            return False, None  # Something else went wrong, unable to validate.
