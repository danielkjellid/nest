from passlib.context import CryptContext
from .auth import AuthService
from nest.records import JWTPairRecord
from nest.database import session
from sqlalchemy import select
from nest.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self):
        ...

    @staticmethod
    def _get_password_hash(raw_password: str) -> str:
        """
        Get the hashed version of a raw password.
        """
        return pwd_context.hash(raw_password)

    @classmethod
    def check_password(cls, raw_password: str, password: str) -> bool:
        """
        Check a users password by comparing the raw version to the hashed version
        stored in the database.
        """
        return pwd_context.verify(raw_password, password)

    @classmethod
    async def authenticate(cls, email: str, password: str) -> JWTPairRecord:
        query = await session.execute(select(User).where(User.email == email))
        user = query.scalars().first()

        if not user:
            raise ValueError("User with provided email does not exist.")

        if not cls.check_password(raw_password=password, password=user.password):
            raise ValueError("Wrong username or password.")

        token_pair = AuthService

        return token_pair
