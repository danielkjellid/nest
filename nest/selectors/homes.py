from nest.models import Home
from nest.records import HomeRecord

from .users import UserSelector


class HomeSelector:
    def __init__(self) -> None:
        ...

    @classmethod
    def all_homes(cls) -> list[HomeRecord]:
        homes = Home.objects.all().prefetch_related("users")
        records = [HomeRecord.from_home(home) for home in homes]

        return records

    @classmethod
    def for_user(cls, user_id: int) -> list[HomeRecord]:
        user = UserSelector.get_user(pk=user_id)

        if user.is_staff or user.is_superuser:
            return cls.all_homes()

        records = []
        available_homes = Home.objects.filter(is_active=True, user=user_id)
        records.extend([HomeRecord.from_home(home) for home in available_homes])

        if user.home:
            primary_home_record = user.home
            # Avoid adding the primary home multiple times.
            if primary_home_record not in records:
                records.append(primary_home_record)

        return records
