from nest.users.models import User
from nest.homes.models import Home

from nest.homes.tests.utils import create_home


def create_user(
    first_name: str = "Test",
    last_name: str = "User",
    home: Home | None = None,
    homes: list[Home] | None = None,
    is_active: bool = True,
    is_staff: bool = False,
    is_superuser: bool = False,
) -> User:
    email = f"{first_name}.{last_name}@example.com"

    if not home:
        home = create_home()

    user, _updated = User.objects.update_or_create(
        email=email,
        first_name=first_name,
        last_name=last_name,
        defaults={
            "home": home,
            "is_active": is_active,
            "is_staff": is_staff,
            "is_superuser": is_superuser,
        },
    )

    homes_to_set = [home]
    if homes:
        homes_to_set += homes

    user.homes.set(homes_to_set)

    return user
