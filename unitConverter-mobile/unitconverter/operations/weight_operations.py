"""Weight conversion operations.

All weight conversions use the kilogram as the base unit.
Each unit's factor represents how many kilograms equal one of that unit.
"""

from unitconverter.models.unit import Unit


WEIGHT_UNITS: tuple[Unit, ...] = (
    Unit(
        id="kilogram",
        name="Kilogram",
        symbol="kg",
        factor=1.0,
        aliases=("kilograms", "kilo", "kilos"),
    ),
    Unit(id="gram", name="Gram", symbol="g", factor=0.001, aliases=("grams",)),
    Unit(
        id="milligram",
        name="Milligram",
        symbol="mg",
        factor=1e-6,
        aliases=("milligrams",),
    ),
    Unit(
        id="metricton",
        name="Metric Ton",
        symbol="t",
        factor=1000.0,
        aliases=("metric tons", "tonne", "tonnes"),
    ),
    Unit(
        id="longton",
        name="Long Ton",
        symbol="LT",
        factor=1016.0469088,
        aliases=("long tons", "imperial ton", "imperial tons"),
    ),
    Unit(
        id="shortton",
        name="Short Ton",
        symbol="ST",
        factor=907.18474,
        aliases=("short tons", "us ton", "us tons"),
    ),
    Unit(
        id="pound",
        name="Pound",
        symbol="lb",
        factor=0.453592,
        aliases=("pounds", "lbs"),
    ),
    Unit(id="ounce", name="Ounce", symbol="oz", factor=0.0283495, aliases=("ounces",)),
    Unit(
        id="carat",
        name="Carat",
        symbol="ct",
        factor=0.0002,
        aliases=("carats", "carrat", "carrats"),
    ),
    Unit(
        id="amu",
        name="Atomic Mass Unit",
        symbol="u",
        factor=1.66053906660e-27,
        aliases=("atomic mass units", "dalton", "daltons"),
    ),
)


def convert_weight(value: float, from_unit_id: str, to_unit_id: str) -> float:
    """Convert a weight value from one unit to another.

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
    """Find a weight unit by its ID.

    Args:
        unit_id: The unique identifier of the unit.

    Returns:
        The matching Unit object.

    Raises:
        ValueError: If the unit ID is not found.
    """
    for unit in WEIGHT_UNITS:
        if unit.id == unit_id:
            return unit
    raise ValueError(f"Unknown weight unit: {unit_id}")
