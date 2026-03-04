"""Converter service that coordinates conversions across all categories."""

from typing import Callable, Optional

from unitconverter.models.category import Category
from unitconverter.models.conversion_result import ConversionResult
from unitconverter.models.unit import Unit
from unitconverter.operations.length_operations import LENGTH_UNITS, convert_length
from unitconverter.operations.temperature_operations import TEMPERATURE_UNITS, convert_temperature
from unitconverter.operations.area_operations import AREA_UNITS, convert_area
from unitconverter.operations.volume_operations import VOLUME_UNITS, convert_volume
from unitconverter.operations.weight_operations import WEIGHT_UNITS, convert_weight
from unitconverter.operations.time_operations import TIME_UNITS, convert_time


class ConverterService:
    """Central service that manages categories and dispatches conversions.

    This service acts as the single entry point for all conversion operations,
    routing each request to the appropriate category-specific converter.
    """

    def __init__(self) -> None:
        """Initialize the converter service with all categories."""
        self._categories: tuple[Category, ...] = (
            Category(id="length", name="Length", icon="📏", units=LENGTH_UNITS),
            Category(
                id="temperature", name="Temperature", icon="🌡️", units=TEMPERATURE_UNITS
            ),
            Category(id="area", name="Area", icon="📐", units=AREA_UNITS),
            Category(id="volume", name="Volume", icon="🧪", units=VOLUME_UNITS),
            Category(id="weight", name="Weight", icon="⚖️", units=WEIGHT_UNITS),
            Category(id="time", name="Time", icon="⏱️", units=TIME_UNITS),
        )

        self._converters: dict[str, Callable[[float, str, str], float]] = {
            "length": convert_length,
            "temperature": convert_temperature,
            "area": convert_area,
            "volume": convert_volume,
            "weight": convert_weight,
            "time": convert_time,
        }

    @property
    def categories(self) -> tuple[Category, ...]:
        """Return all available categories."""
        return self._categories

    def get_category(self, category_id: str) -> Optional[Category]:
        """Get a category by its ID.

        Args:
            category_id: The unique identifier of the category.

        Returns:
            The Category if found, None otherwise.
        """
        for category in self._categories:
            if category.id == category_id:
                return category
        return None

    def convert(
        self,
        value: float,
        category_id: str,
        from_unit_id: str,
        to_unit_id: str,
    ) -> ConversionResult:
        """Perform a unit conversion.

        Args:
            value: The numeric value to convert.
            category_id: The category of units.
            from_unit_id: The source unit ID.
            to_unit_id: The target unit ID.

        Returns:
            A ConversionResult with the converted value.

        Raises:
            ValueError: If the category or units are not found.
        """
        converter = self._converters.get(category_id)
        if converter is None:
            raise ValueError(f"Unknown category: {category_id}")

        category = self.get_category(category_id)
        if category is None:
            raise ValueError(f"Category not found: {category_id}")

        from_unit = category.get_unit_by_id(from_unit_id)
        to_unit = category.get_unit_by_id(to_unit_id)

        if from_unit is None:
            raise ValueError(
                f"Unknown unit '{from_unit_id}' in category '{category_id}'"
            )
        if to_unit is None:
            raise ValueError(f"Unknown unit '{to_unit_id}' in category '{category_id}'")

        result_value = converter(value, from_unit_id, to_unit_id)

        return ConversionResult(
            from_value=value,
            to_value=result_value,
            from_unit_symbol=from_unit.symbol,
            to_unit_symbol=to_unit.symbol,
            from_unit_name=from_unit.name,
            to_unit_name=to_unit.name,
            category_id=category_id,
        )
