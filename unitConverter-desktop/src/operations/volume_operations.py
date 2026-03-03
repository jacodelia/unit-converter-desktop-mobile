"""Volume conversion operations.

All volume conversions use the cubic meter as the base unit.
Each unit's factor represents how many cubic meters equal one of that unit.
"""

from src.models.unit import Unit


VOLUME_UNITS: tuple[Unit, ...] = (
    Unit(
        id="cubicmeter",
        name="Cubic Meter",
        symbol="m³",
        factor=1.0,
        aliases=("cubic meters", "cu meter", "cu m"),
    ),
    Unit(
        id="cubickilometer",
        name="Cubic Kilometer",
        symbol="km³",
        factor=1e9,
        aliases=("cubic kilometers", "cu kilometer", "cu km"),
    ),
    Unit(
        id="cubiccentimeter",
        name="Cubic Centimeter",
        symbol="cm³",
        factor=1e-6,
        aliases=("cubic centimeters", "cu centimeter", "cu cm", "cc"),
    ),
    Unit(
        id="cubicmillimeter",
        name="Cubic Millimeter",
        symbol="mm³",
        factor=1e-9,
        aliases=("cubic millimeters", "cu millimeter", "cu mm"),
    ),
    Unit(
        id="liter",
        name="Liter",
        symbol="L",
        factor=0.001,
        aliases=("liters", "litre", "litres", "l"),
    ),
    Unit(
        id="milliliter",
        name="Milliliter",
        symbol="mL",
        factor=1e-6,
        aliases=("milliliters", "millilitre", "millilitres", "ml"),
    ),
    Unit(
        id="usgallon",
        name="US Gallon",
        symbol="gal",
        factor=0.00378541,
        aliases=("us gallons", "gallon", "gallons", "us galon"),
    ),
    Unit(
        id="usquart",
        name="US Quart",
        symbol="qt",
        factor=0.000946353,
        aliases=("us quarts", "quart", "quarts"),
    ),
    Unit(
        id="uspint",
        name="US Pint",
        symbol="pt",
        factor=0.000473176,
        aliases=("us pints", "pint", "pints"),
    ),
    Unit(
        id="uscup",
        name="US Cup",
        symbol="cup",
        factor=0.000236588,
        aliases=("us cups", "cup", "cups"),
    ),
    Unit(
        id="usfluidounce",
        name="US Fluid Ounce",
        symbol="fl oz",
        factor=2.9574e-5,
        aliases=("us fluid ounces", "fluid ounce", "fluid ounces", "fl oz"),
    ),
)


def convert_volume(value: float, from_unit_id: str, to_unit_id: str) -> float:
    """Convert a volume value from one unit to another.

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
    """Find a volume unit by its ID.

    Args:
        unit_id: The unique identifier of the unit.

    Returns:
        The matching Unit object.

    Raises:
        ValueError: If the unit ID is not found.
    """
    for unit in VOLUME_UNITS:
        if unit.id == unit_id:
            return unit
    raise ValueError(f"Unknown volume unit: {unit_id}")
