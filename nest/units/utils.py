from decimal import Decimal
from typing import Callable

from .enums import UnitType
from .records import UnitRecord


def convert_unit_quantity(
    *,
    quantity: Decimal,
    from_unit: UnitRecord,
    to_unit: UnitRecord,
    weight_piece: Decimal | None = None,
    weight_ml: Decimal | None = None,
):
    """
    Try to convert a quantity in one unit to a quantity in another unit.
    Returns None of the conversion was not possible.
    """

    conversions: dict[UnitType, dict[UnitType, Callable[[Decimal], Decimal]]] = {
        UnitType.WEIGHT: {
            UnitType.PIECES: lambda x: x / weight_piece,
            UnitType.VOLUME: lambda x: x / weight_ml,
        },
        UnitType.VOLUME: {
            UnitType.PIECES: lambda x: (x * weight_ml) / weight_piece,
            UnitType.WEIGHT: lambda x: x * weight_ml,
        },
        UnitType.PIECES: {
            UnitType.WEIGHT: lambda x: x * weight_piece,
            UnitType.VOLUME: lambda x: (x * weight_piece) / weight_ml,
        },
    }

    to_type = to_unit.unit_type
    from_type = from_unit.unit_type
    quantity_in_base = quantity * from_unit.base_factor

    # Same unit types, so it can be converted directly.
    if from_type == to_type:
        return quantity_in_base / to_unit.base_factor

    # Can't convert other types to length
    if to_type == UnitType.LENGTH:
        return None

    try:
        # Convert to base unit and convert
        converted_in_base = conversions[from_type][to_type](quantity_in_base)
        return converted_in_base / to_unit.base_factor

    except (TypeError, KeyError, ZeroDivisionError) as exc:
        raise RuntimeError(
            f"Failed to convert quantity {quantity} from unit {from_unit} to unit {to_unit}"
        ) from exc
