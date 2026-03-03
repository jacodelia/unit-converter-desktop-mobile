"""Conversion result model for storing conversion outcomes."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ConversionResult:
    """Represents the result of a unit conversion.

    Attributes:
        from_value: The input value.
        to_value: The converted output value.
        from_unit_symbol: Symbol of the source unit.
        to_unit_symbol: Symbol of the target unit.
        from_unit_name: Name of the source unit.
        to_unit_name: Name of the target unit.
        category_id: ID of the category this conversion belongs to.
        timestamp: When the conversion was performed.
    """

    from_value: float
    to_value: float
    from_unit_symbol: str
    to_unit_symbol: str
    from_unit_name: str
    to_unit_name: str
    category_id: str
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def display_string(self) -> str:
        """Return a human-readable string of the conversion."""
        from_formatted = self._format_number(self.from_value)
        to_formatted = self._format_number(self.to_value)
        return (
            f"{from_formatted} {self.from_unit_symbol} "
            f"→ {to_formatted} {self.to_unit_symbol}"
        )

    @property
    def time_string(self) -> str:
        """Return a formatted time string."""
        return self.timestamp.strftime("%H:%M:%S")

    @staticmethod
    def _format_number(value: float) -> str:
        """Format a number for display, removing trailing zeros.

        Args:
            value: The number to format.

        Returns:
            Formatted string representation.
        """
        if value == 0:
            return "0"
        formatted = f"{value:.10g}"
        return formatted
