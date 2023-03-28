from nest.exceptions import ApplicationError
from nest.models import User
from nest.records import UserRecord


class UserSelector:
    @classmethod
    def get_user(cls, pk: int) -> UserRecord:
        """
        Get a user instance.
        """
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist as exc:
            raise ApplicationError(message="User does not exist.") from exc

        return UserRecord.from_user(user)
