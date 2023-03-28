from nest.exceptions import ApplicationError
from nest.models import User
from nest.records import UserRecord


class UserSelector:
    @classmethod
    def get_user(cls, pk: int) -> UserRecord:
        """
        Get a user instance.

        Note: this performs an additional lookup to home to populate the record, so do
        not use this in a loop.
        """
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist as exc:
            raise ApplicationError(message="User does not exist.") from exc

        return UserRecord.from_user(user)
