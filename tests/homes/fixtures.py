from decimal import Decimal
from typing import Any, Callable, TypedDict

import pytest

from nest.homes.models import Home


class HomeSpec(TypedDict, total=False):
    street_address: str
    zip_code: str
    zip_place: str
    num_residents: int
    num_weeks_recipe_rotation: int
    weekly_budget: Decimal
    is_active: bool


CreateHome = Callable[[HomeSpec], Home]


@pytest.fixture
def default_home_spec() -> HomeSpec:
    return HomeSpec(
        street_address="Example road",
        zip_code="1234",
        zip_place="Oslo",
        num_residents=4,
        num_weeks_recipe_rotation=2,
        weekly_budget=Decimal("2500"),
        is_active=True,
    )


@pytest.fixture
def create_home_from_spec(db: Any) -> CreateHome:
    def _create_home(spec: HomeSpec) -> Home:
        home, _created = Home.objects.get_or_create(**spec)
        return home

    return _create_home


@pytest.fixture
def home(create_instance, create_home_from_spec, default_home_spec) -> Home:
    return create_instance(
        create_callback=create_home_from_spec,
        default_spec=default_home_spec,
        marker_name="home",
    )


@pytest.fixture
def homes(
    create_instances, default_home_spec, create_home_from_spec
) -> dict[str, Home]:
    return create_instances(
        create_callback=create_home_from_spec,
        default_spec=default_home_spec,
        marker_name="homes",
    )
