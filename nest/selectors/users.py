from nest.exceptions import ApplicationError
from nest.models import User
from nest.records import UserRecord


class UserSelector:
    @classmethod
    def get_user(cls, pk: int) -> UserRecord:
        """
        Get a user instance.
        """
        user = User.objects.filter(id=pk).select_related("home").first()

        if not user:
            raise ApplicationError(message="User does not exist.")

        return UserRecord.from_user(user)

    @classmethod
    def all_users(cls) -> list[UserRecord]:
        """
        Get a list of all users.
        """

        users = User.objects.all().select_related("home")
        return [UserRecord.from_user(user) for user in users]
