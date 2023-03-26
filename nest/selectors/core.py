from django.http import HttpRequest
from nest.records import CoreInitialPropsRecord, UserRecord, CoreConfigRecord
from .homes import HomeSelector


class CoreSelector:
    ...

    @classmethod
    def initial_props(cls, request: HttpRequest) -> CoreInitialPropsRecord | None:

        if not request.user or not request.user.is_authenticated:
            return None

        user = request.user
        user_record = UserRecord.from_user(user)
        available_homes = HomeSelector.for_user(user_id=user.id)

        return CoreInitialPropsRecord(
            config=CoreConfigRecord(is_production=False),
            current_user=user_record,
            available_homes=available_homes,
        )
