from nest.models import Home
from nest.records import HomeRecord, UserRecord

from .users import UserSelector


class HomeSelector:
    @classmethod
    def all_homes(cls) -> list[HomeRecord]:
        """
        Get all homes regardless of active state.
        """

        homes = Home.objects.all()
        records = [HomeRecord.from_home(home) for home in homes]

        return records

    @classmethod
    def user_homes(cls, user: UserRecord) -> list[HomeRecord]:
        """
        Get all available homes for a specific user.
        """

        if user.is_staff or user.is_superuser:
            return cls.all_homes()

        records = []
        available_homes_for_user = Home.objects.filter(
            is_active=True, users__in=[user.id]
        )
        records.extend(
            [HomeRecord.from_home(home) for home in available_homes_for_user]
        )

        if user.home:
            primary_home_record = user.home
            # Avoid adding the primary home multiple times.
            if primary_home_record not in records:
                records.append(primary_home_record)

        return records
