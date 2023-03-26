from nest.models import User, Home
from nest.records import HomeRecord
from nest.exceptions import ApplicationError


class HomeSelector:
    def __init__(self):
        ...

    @classmethod
    def all(cls) -> list[HomeRecord]:
        homes = Home.objects.all().prefetch_related("users")
        records = [HomeRecord.from_home(home) for home in homes]

        return records

    @classmethod
    def for_user(cls, user_id: int) -> list[HomeRecord]:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ApplicationError(message="User does not exist.")

        if user.is_staff or user.is_superuser:
            return cls.all()

        primary_home_record = HomeRecord.from_home(user.home)
        available_homes = user.homes.filter(is_active=True)
        records = [HomeRecord.from_home(home) for home in available_homes]
        records.append(primary_home_record)

        return records
