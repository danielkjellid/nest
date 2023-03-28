from nest.models import Home
from nest.records import HomeRecord, UserRecord
from django.db.models import Q
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

        # Return all homes in the app for staff users.
        if user.is_staff or user.is_superuser:
            return cls.all_homes()

        # Get home set as primary and all available homes.
        available_homes_for_user = Home.objects.active().filter(
            Q(users__in=[user.id]) | Q(user=user.id)
        )
        records = [HomeRecord.from_home(home) for home in available_homes_for_user]

        return records
