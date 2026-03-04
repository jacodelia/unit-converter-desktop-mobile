"""Area conversion operations.

All area conversions use the square meter as the base unit.
Each unit's factor represents how many square meters equal one of that unit.
"""

from unitconverter.models.unit import Unit


AREA_UNITS: tuple[Unit, ...] = (
    Unit(
        id="sqmeter",
        name="Square Meter",
        symbol="m²",
        factor=1.0,
        aliases=("square meters", "sq meter", "sq meters", "sq m"),
    ),
    Unit(
        id="sqkilometer",
        name="Square Kilometer",
        symbol="km²",
        factor=1e6,
        aliases=("square kilometers", "sq kilometer", "sq km"),
    ),
    Unit(
        id="sqcentimeter",
        name="Square Centimeter",
        symbol="cm²",
        factor=1e-4,
        aliases=("square centimeters", "sq centimeter", "sq cm"),
    ),
    Unit(
        id="sqmillimeter",
        name="Square Millimeter",
        symbol="mm²",
        factor=1e-6,
        aliases=("square millimeters", "sq millimeter", "sq mm"),
    ),
    Unit(
        id="sqmicrometer",
        name="Square Micrometer",
        symbol="μm²",
        factor=1e-12,
        aliases=("square micrometers", "sq micrometer"),
    ),
    Unit(
        id="hectare", name="Hectare", symbol="ha", factor=10000.0, aliases=("hectares",)
    ),
    Unit(
        id="sqmile",
        name="Square Mile",
        symbol="mi²",
        factor=2589988.110336,
        aliases=("square miles", "sq mile", "sq mi"),
    ),
    Unit(
        id="sqyard",
        name="Square Yard",
        symbol="yd²",
        factor=0.836127,
        aliases=("square yards", "sq yard", "sq yd"),
    ),
    Unit(
        id="sqfoot",
        name="Square Foot",
        symbol="ft²",
        factor=0.092903,
        aliases=("square feet", "sq foot", "sq ft"),
    ),
    Unit(
        id="sqinch",
        name="Square Inch",
        symbol="in²",
        factor=0.00064516,
        aliases=("square inches", "sq inch", "sq in"),
    ),
    Unit(id="acre", name="Acre", symbol="ac", factor=4046.8564224, aliases=("acres",)),
)


def convert_area(value: float, from_unit_id: str, to_unit_id: str) -> float:
    """Convert an area value from one unit to another.

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
    """Find an area unit by its ID.

    Args:
        unit_id: The unique identifier of the unit.

    Returns:
        The matching Unit object.

    Raises:
        ValueError: If the unit ID is not found.
    """
    for unit in AREA_UNITS:
        if unit.id == unit_id:
            return unit
    raise ValueError(f"Unknown area unit: {unit_id}")
