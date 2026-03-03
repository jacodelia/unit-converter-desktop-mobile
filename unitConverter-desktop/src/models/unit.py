"""Unit model representing a single unit of measurement."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Unit:
    """Represents a single unit of measurement.

    Attributes:
        id: Unique identifier for the unit (e.g., 'meter', 'kilogram').
        name: Display name of the unit (e.g., 'Meter', 'Kilogram').
        symbol: Abbreviated symbol (e.g., 'm', 'kg').
        factor: Conversion factor relative to the base unit of its category.
                For temperature units, this is not used directly.
        aliases: Alternative names for search matching.
    """

    id: str
    name: str
    symbol: str
    factor: float = 1.0
    aliases: tuple[str, ...] = field(default_factory=tuple)

    def matches_search(self, query: str) -> bool:
        """Check if this unit matches a search query (case-insensitive).

        Args:
            query: The search string to match against.

        Returns:
            True if the unit matches the query.
        """
        query_lower = query.lower().strip()
        if not query_lower:
            return True

        searchable = (
            self.id.lower(),
            self.name.lower(),
            self.symbol.lower(),
            *(alias.lower() for alias in self.aliases),
        )

        return any(query_lower in term for term in searchable)
