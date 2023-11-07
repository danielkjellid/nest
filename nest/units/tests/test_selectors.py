from decimal import Decimal

import pytest

from nest.core.exceptions import ApplicationError

from ..selectors import (
    get_unit_by_abbreviation,
    get_unit_highest_normalized_quantity,
    get_unit_lowest_normalized_quantity,
    get_unit_normalized_price,
    get_unit_normalized_quantity,
    get_units,
)
from .utils import create_units, get_unit

pytestmark = pytest.mark.django_db


def test_get_units(django_assert_num_queries):
    """
    Test that all_units selector returns all units available within query limits.
    """
    create_units()  # 26 units.

    with django_assert_num_queries(1):
        units = get_units()

    assert len(units) == 26


def test_get_unit_by_abbreviation(django_assert_num_queries):
    """
    Test that the get_unit_from_abbreviation correctly retrieves the right unit,
    withing query limits, as well as raises ApplicationError if unit does not exist.
    """
    create_units()

    with django_assert_num_queries(1):
        kg = get_unit_by_abbreviation(abbreviation="kg")

    assert kg is not None
    assert kg.abbreviation == "kg"

    with django_assert_num_queries(1):
        g = get_unit_by_abbreviation(abbreviation="g")

    assert g is not None
    assert g.abbreviation == "g"

    with pytest.raises(ApplicationError):
        get_unit_by_abbreviation(abbreviation="doesnotexist")


@pytest.mark.parametrize(
    "from_abbr, to_abbr, mocks_called",
    (
        ("kg", "g", True),
        ("l", "ml", True),
        ("dl", "ml", True),
        ("m", "cm", True),
        ("stk", "pk", False),
    ),
)
def test_selector_get_unit_lowest_normalized_quantity(
    from_abbr,
    to_abbr,
    mocks_called,
    unit_records_by_abbreviation,
    mocker,
):
    """
    Test that the get_unit_lowest_normalized_quantity converts to the lowest possible
    unit in the same hierarchy.
    """
    records = unit_records_by_abbreviation
    quantity = Decimal("400")
    convert_mock = mocker.patch("nest.units.selectors.convert_unit_quantity")
    get_unit_mock = mocker.patch(
        "nest.units.selectors.get_unit_by_abbreviation", return_value=records[to_abbr]
    )

    get_unit_lowest_normalized_quantity(
        quantity=quantity,
        unit=records[from_abbr],
    )

    if mocks_called:
        get_unit_mock.assert_called_once_with(abbreviation=to_abbr)
        convert_mock.assert_called_once_with(
            quantity=quantity,
            from_unit=records[from_abbr],
            to_unit=records[to_abbr],
        )
    else:
        convert_mock.assert_not_called()
        get_unit_mock.assert_not_called()


@pytest.mark.parametrize(
    "from_abbr, to_abbr, mocks_called",
    (
        ("g", "kg", True),
        ("ml", "l", True),
        ("dl", "l", True),
        ("cm", "m", True),
        ("stk", "pk", False),
    ),
)
def test_selector_get_unit_highest_normalized_quantity(
    from_abbr, to_abbr, mocks_called, unit_records_by_abbreviation, mocker
):
    """
    Test that the get_unit_highest_normalized_quantity converts to the highest possible
    unit in the same hierarchy.
    """
    records = unit_records_by_abbreviation
    quantity = Decimal("200")
    convert_mock = mocker.patch("nest.units.selectors.convert_unit_quantity")
    get_unit_mock = mocker.patch(
        "nest.units.selectors.get_unit_by_abbreviation", return_value=records[to_abbr]
    )

    get_unit_highest_normalized_quantity(quantity=quantity, unit=records[from_abbr])

    if mocks_called:
        get_unit_mock.assert_called_once_with(abbreviation=to_abbr)
        convert_mock.assert_called_once_with(
            quantity=quantity,
            from_unit=records[from_abbr],
            to_unit=records[to_abbr],
        )
    else:
        convert_mock.assert_not_called()
        get_unit_mock.assert_not_called()


@pytest.mark.parametrize(
    "quantity, expected_mock_call",
    (
        (Decimal("100"), "highest"),
        (Decimal("0.9"), "lowest"),
        (Decimal("0.9999999999"), "lowest"),
        (Decimal("1.00000001"), "highest"),
    ),
)
def test_selector_get_unit_normalized_quantity(quantity, expected_mock_call, mocker):
    """
    Test that the get_unit_normalized_quantity calls the correct normalize function
    based on if the given quantity is greater than 1.
    """
    lowest_mock = mocker.patch(
        "nest.units.selectors.get_unit_lowest_normalized_quantity"
    )
    highest_mock = mocker.patch(
        "nest.units.selectors.get_unit_highest_normalized_quantity"
    )
    unit = get_unit(abbreviation="g")

    get_unit_normalized_quantity(quantity=quantity, unit=unit)

    if expected_mock_call == "highest":
        lowest_mock.assert_not_called()
        highest_mock.assert_called_once_with(quantity=quantity, unit=unit)
    elif expected_mock_call == "lowest":
        lowest_mock.assert_called_once_with(quantity=quantity, unit=unit)
        highest_mock.assert_not_called()


@pytest.mark.parametrize(
    "quantity, expected",
    (
        (Decimal("10"), Decimal("10")),
        (Decimal("25"), Decimal("4")),
        (Decimal("1000"), Decimal("0.1")),
        (Decimal("300"), Decimal("0.33")),
    ),
)
def test_selector_get_unit_normalized_price(quantity, expected, mocker):
    """
    Test that we're able to correctly calculate a unit price.
    """
    unit = get_unit(abbreviation="g")
    normalized_unit_mock = mocker.patch(
        "nest.units.selectors.get_unit_highest_normalized_quantity",
        return_value=(quantity, unit),
    )

    price, _unit = get_unit_normalized_price(
        price=Decimal(100), quantity=quantity, unit=unit
    )

    assert normalized_unit_mock.called_once_with(quantity=quantity, unit=unit)
    assert price == expected
