"""Temperature conversion operations.

Temperature conversions use special formulas instead of simple factors,
as the relationship between temperature scales is not purely multiplicative.
"""

from src.models.unit import Unit


TEMPERATURE_UNITS: tuple[Unit, ...] = (
    Unit(
        id="celsius",
        name="Celsius",
        symbol="°C",
        factor=0.0,
        aliases=("centigrade", "c"),
    ),
    Unit(id="kelvin", name="Kelvin", symbol="K", factor=0.0, aliases=("k",)),
    Unit(id="fahrenheit", name="Fahrenheit", symbol="°F", factor=0.0, aliases=("f",)),
)


def convert_temperature(value: float, from_unit_id: str, to_unit_id: str) -> float:
    """Convert a temperature value from one unit to another.

    Conversion flow: source -> Celsius -> target

    Args:
        value: The numeric value to convert.
        from_unit_id: The ID of the source unit.
        to_unit_id: The ID of the target unit.

    Returns:
        The converted value.

    Raises:
        ValueError: If either unit ID is not recognized.
    """
    _validate_unit(from_unit_id)
    _validate_unit(to_unit_id)

    if from_unit_id == to_unit_id:
        return value

    celsius = _to_celsius(value, from_unit_id)
    return _from_celsius(celsius, to_unit_id)


def _to_celsius(value: float, unit_id: str) -> float:
    """Convert a temperature value to Celsius.

    Args:
        value: The temperature value.
        unit_id: The source unit ID.

    Returns:
        The value in Celsius.
    """
    if unit_id == "celsius":
        return value
    elif unit_id == "fahrenheit":
        return (value - 32.0) * 5.0 / 9.0
    elif unit_id == "kelvin":
        return value - 273.15
    raise ValueError(f"Unknown temperature unit: {unit_id}")


def _from_celsius(celsius: float, unit_id: str) -> float:
    """Convert a Celsius value to the target unit.

    Args:
        celsius: The temperature in Celsius.
        unit_id: The target unit ID.

    Returns:
        The converted value.
    """
    if unit_id == "celsius":
        return celsius
    elif unit_id == "fahrenheit":
        return celsius * 9.0 / 5.0 + 32.0
    elif unit_id == "kelvin":
        return celsius + 273.15
    raise ValueError(f"Unknown temperature unit: {unit_id}")


def _validate_unit(unit_id: str) -> None:
    """Validate that a unit ID exists in temperature units.

    Args:
        unit_id: The unit ID to validate.

    Raises:
        ValueError: If the unit ID is not found.
    """
    valid_ids = {u.id for u in TEMPERATURE_UNITS}
    if unit_id not in valid_ids:
        raise ValueError(f"Unknown temperature unit: {unit_id}")
