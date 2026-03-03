"""Category model representing a group of related units."""

from dataclasses import dataclass, field
from typing import Optional

from src.models.unit import Unit


@dataclass(frozen=True)
class Category:
    """Represents a category of units (e.g., Length, Temperature).

    Attributes:
        id: Unique identifier for the category.
        name: Display name of the category.
        icon: Emoji or icon representation.
        units: Tuple of Unit objects belonging to this category.
    """

    id: str
    name: str
    icon: str
    units: tuple[Unit, ...] = field(default_factory=tuple)

    @property
    def default_from_unit(self) -> Optional[Unit]:
        """Return the first unit as the default 'from' unit."""
        return self.units[0] if self.units else None

    @property
    def default_to_unit(self) -> Optional[Unit]:
        """Return the second unit as the default 'to' unit."""
        if len(self.units) >= 2:
            return self.units[1]
        return self.units[0] if self.units else None

    def get_unit_by_id(self, unit_id: str) -> Optional[Unit]:
        """Find a unit by its ID.

        Args:
            unit_id: The unique identifier of the unit.

        Returns:
            The Unit if found, None otherwise.
        """
        for unit in self.units:
            if unit.id == unit_id:
                return unit
        return None

    def search_units(self, query: str) -> list[Unit]:
        """Search for units matching a query string.

        Args:
            query: The search string (case-insensitive).

        Returns:
            List of matching Unit objects.
        """
        return [unit for unit in self.units if unit.matches_search(query)]
