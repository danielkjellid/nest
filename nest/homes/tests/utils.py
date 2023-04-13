from decimal import Decimal

from nest.homes.models import Home


def create_home(
    street_address: str = "Address 1",
    zip_code: str = "0000",
    zip_place="Nowhere",
    num_residents: int = 2,
    num_weeks_recipe_rotation: int = 2,
    weekly_budget: str = "1000.00",
    is_active: bool = True,
) -> Home:
    home, _created = Home.objects.get_or_create(
        street_address=street_address,
        zip_code=zip_code,
        zip_place=zip_place,
        num_residents=num_residents,
        num_weeks_recipe_rotation=num_weeks_recipe_rotation,
        weekly_budget=Decimal(weekly_budget),
        is_active=is_active,
    )
    return home
