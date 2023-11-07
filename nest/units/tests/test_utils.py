from decimal import Decimal

import pytest

from ..utils import convert_unit_quantity


@pytest.mark.parametrize(
    "quantity, from_unit," "expected_quantity, to_unit," "piece_weight, ml_weight",
    (
        (Decimal(500), "g", Decimal("0.5"), "kg", None, None),
        (Decimal(5), "kg", Decimal(5000), "g", None, None),
        (Decimal(750), "g", Decimal("1.5"), "stk", Decimal(500), None),
        (Decimal(800), "g", Decimal(100), "ml", None, Decimal(8)),
        (Decimal(200), "ml", Decimal(400), "g", None, Decimal(2)),
        (Decimal(400), "ml", Decimal(2), "stk", Decimal(400), Decimal(2)),
        (Decimal(2), "stk", Decimal(300), "g", Decimal(150), None),
        (Decimal(2), "stk", Decimal("0.02"), "l", Decimal(25), Decimal("2.5")),
    ),
)
@pytest.mark.django_db
def test_util_convert_unit_quantity(
    quantity,
    from_unit,
    to_unit,
    piece_weight,
    ml_weight,
    expected_quantity,
    unit_records_by_abbreviation,
    django_assert_num_queries,
):
    from_unit, to_unit = (
        unit_records_by_abbreviation[from_unit],
        unit_records_by_abbreviation[to_unit],
    )

    with django_assert_num_queries(0):
        converted_quantity = convert_unit_quantity(
            quantity=quantity,
            from_unit=from_unit,
            to_unit=to_unit,
            weight_piece=piece_weight,
            weight_ml=ml_weight,
        )
    assert converted_quantity == expected_quantity
