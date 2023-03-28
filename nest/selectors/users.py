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
        user = User.objects.filter(id=pk).select_related("home").first()

        if not user:
            raise ApplicationError(message="User does not exist.")

        return UserRecord.from_user(user)
