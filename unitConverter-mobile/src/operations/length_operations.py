"""Length conversion operations.

All length conversions use the meter as the base unit.
Each unit's factor represents how many meters equal one of that unit.
"""

from src.models.unit import Unit


LENGTH_UNITS: tuple[Unit, ...] = (
    Unit(
        id="meter",
        name="Meter",
        symbol="m",
        factor=1.0,
        aliases=("meters", "metre", "metres"),
    ),
    Unit(
        id="kilometer",
        name="Kilometer",
        symbol="km",
        factor=1000.0,
        aliases=("kilometers", "kilometre", "kilometres", "km"),
    ),
    Unit(
        id="centimeter",
        name="Centimeter",
        symbol="cm",
        factor=0.01,
        aliases=("centimeters", "centimetre", "centimetres"),
    ),
    Unit(
        id="millimeter",
        name="Millimeter",
        symbol="mm",
        factor=0.001,
        aliases=("millimeters", "millimetre", "millimetres"),
    ),
    Unit(
        id="micrometer",
        name="Micrometer",
        symbol="μm",
        factor=1e-6,
        aliases=("micrometers", "micrometre", "micrometres", "micron"),
    ),
    Unit(
        id="nanometer",
        name="Nanometer",
        symbol="nm",
        factor=1e-9,
        aliases=("nanometers", "nanometre", "nanometres"),
    ),
    Unit(id="mile", name="Mile", symbol="mi", factor=1609.344, aliases=("miles",)),
    Unit(id="yard", name="Yard", symbol="yd", factor=0.9144, aliases=("yards",)),
    Unit(id="foot", name="Foot", symbol="ft", factor=0.3048, aliases=("feet",)),
    Unit(id="inch", name="Inch", symbol="in", factor=0.0254, aliases=("inches",)),
    Unit(
        id="lightyear",
        name="Light Year",
        symbol="ly",
        factor=9.461e15,
        aliases=("light years", "lightyears", "light-year", "light-years"),
    ),
)


def convert_length(value: float, from_unit_id: str, to_unit_id: str) -> float:
    """Convert a length value from one unit to another.

    Args:
        value: The numeric value to convert.
        from_unit_id: The ID of the source unit.
        to_unit_id: The ID of the target unit.

    Returns:
        The converted value.

    Raises:
        ValueError: If either unit ID is not found.
    """
    from_unit = _find_unit(from_unit_id)
    to_unit = _find_unit(to_unit_id)

    base_value = value * from_unit.factor
    return base_value / to_unit.factor


def _find_unit(unit_id: str) -> Unit:
    """Find a length unit by its ID.

    Args:
        unit_id: The unique identifier of the unit.

    Returns:
        The matching Unit object.

    Raises:
        ValueError: If the unit ID is not found.
    """
    for unit in LENGTH_UNITS:
        if unit.id == unit_id:
            return unit
    raise ValueError(f"Unknown length unit: {unit_id}")
