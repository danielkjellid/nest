from nest.core.exceptions import ApplicationError

from .models import User as UserModel
from .types import User


def get_user(*, pk: int) -> User:
    """
    Get a user instance.
    """
    user = UserModel.objects.filter(id=pk).select_related("home").first()

    if not user:
        raise ApplicationError(message="User does not exist.")

    return User.from_user(user)


def get_users() -> list[User]:
    """
    Get a list of all users.
    """

    users = UserModel.objects.all().select_related("home")
    return [User.from_user(user) for user in users]
