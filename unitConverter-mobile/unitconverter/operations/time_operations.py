"""Time conversion operations.

All time conversions use the second as the base unit.
Each unit's factor represents how many seconds equal one of that unit.
"""

from unitconverter.models.unit import Unit


TIME_UNITS: tuple[Unit, ...] = (
    Unit(
        id="second",
        name="Second",
        symbol="s",
        factor=1.0,
        aliases=("seconds", "sec", "secs"),
    ),
    Unit(
        id="millisecond",
        name="Millisecond",
        symbol="ms",
        factor=0.001,
        aliases=("milliseconds",),
    ),
    Unit(
        id="microsecond",
        name="Microsecond",
        symbol="μs",
        factor=1e-6,
        aliases=("microseconds",),
    ),
    Unit(
        id="nanosecond",
        name="Nanosecond",
        symbol="ns",
        factor=1e-9,
        aliases=("nanoseconds",),
    ),
    Unit(
        id="picosecond",
        name="Picosecond",
        symbol="ps",
        factor=1e-12,
        aliases=("picoseconds",),
    ),
    Unit(id="minute", name="Minute", symbol="min", factor=60.0, aliases=("minutes",)),
    Unit(
        id="hour",
        name="Hour",
        symbol="h",
        factor=3600.0,
        aliases=("hours", "hr", "hrs"),
    ),
    Unit(id="day", name="Day", symbol="d", factor=86400.0, aliases=("days",)),
    Unit(id="week", name="Week", symbol="wk", factor=604800.0, aliases=("weeks",)),
    Unit(id="month", name="Month", symbol="mo", factor=2592000.0, aliases=("months",)),
    Unit(id="year", name="Year", symbol="yr", factor=31536000.0, aliases=("years",)),
)


def convert_time(value: float, from_unit_id: str, to_unit_id: str) -> float:
    """Convert a time value from one unit to another.

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
    """Find a time unit by its ID.

    Args:
        unit_id: The unique identifier of the unit.

    Returns:
        The matching Unit object.

    Raises:
        ValueError: If the unit ID is not found.
    """
    for unit in TIME_UNITS:
        if unit.id == unit_id:
            return unit
    raise ValueError(f"Unknown time unit: {unit_id}")
