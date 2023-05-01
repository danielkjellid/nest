from nest.core.exceptions import ApplicationError

from .models import User
from .records import UserRecord


def get_user(pk: int) -> UserRecord:
    """
    Get a user instance.
    """
    user = User.objects.filter(id=pk).select_related("home").first()

    if not user:
        raise ApplicationError(message="User does not exist.")

    return UserRecord.from_user(user)


def get_users() -> list[UserRecord]:
    """
    Get a list of all users.
    """

    users = User.objects.all().select_related("home")
    return [UserRecord.from_user(user) for user in users]
