"""Search service for natural language unit search and parsing.

Handles queries like:
    - "from kilometers to meters"
    - "kilometer to meter"
    - "km to m"
    - "length"
    - "meter"
"""

import re
from dataclasses import dataclass
from typing import Optional

from src.models.category import Category
from src.models.unit import Unit
from src.services.converter_service import ConverterService


@dataclass
class SearchResult:
    """Result of a search/parse operation.

    Attributes:
        category: The matched category (if any).
        from_unit: The matched source unit (if any).
        to_unit: The matched target unit (if any).
        matched_units: All units matching the query across categories.
    """

    category: Optional[Category] = None
    from_unit: Optional[Unit] = None
    to_unit: Optional[Unit] = None
    matched_units: Optional[list[tuple[Category, Unit]]] = None

    def __post_init__(self) -> None:
        if self.matched_units is None:
            self.matched_units = []

    @property
    def is_conversion_query(self) -> bool:
        """True if both from and to units were identified."""
        return self.from_unit is not None and self.to_unit is not None

    @property
    def has_results(self) -> bool:
        """True if any results were found."""
        return (
            self.category is not None
            or self.from_unit is not None
            or (self.matched_units is not None and len(self.matched_units) > 0)
        )


class SearchService:
    """Service for parsing and searching unit conversion queries.

    Supports natural language patterns like:
        - "from X to Y" - identifies source and target units
        - "X to Y" - identifies source and target units
        - "meter" - searches for matching units
        - "length" - matches a category
    """

    # Pattern: "from X to Y" or "X to Y"
    _CONVERSION_PATTERN = re.compile(
        r"(?:from\s+)?(.+?)\s+to\s+(.+)",
        re.IGNORECASE,
    )

    def __init__(self, converter_service: ConverterService) -> None:
        """Initialize with a converter service for category/unit access.

        Args:
            converter_service: The converter service instance.
        """
        self._converter = converter_service

    def search(self, query: str) -> SearchResult:
        """Parse and search for units matching the query.

        Args:
            query: The search string (case-insensitive).

        Returns:
            A SearchResult with matched categories, units, etc.
        """
        query = query.strip()
        if not query:
            return SearchResult()

        # Try to parse as a conversion query (e.g., "km to miles")
        conversion_match = self._CONVERSION_PATTERN.match(query)
        if conversion_match:
            from_text = conversion_match.group(1).strip()
            to_text = conversion_match.group(2).strip()
            return self._resolve_conversion(from_text, to_text)

        # Try to match a category name
        category = self._find_category(query)
        if category:
            return SearchResult(category=category)

        # Search for units across all categories
        matched_units = self._search_all_units(query)
        if matched_units:
            # If all matches are in the same category, set that category
            categories = {cat.id for cat, _ in matched_units}
            category = matched_units[0][0] if len(categories) == 1 else None
            return SearchResult(
                category=category,
                from_unit=matched_units[0][1] if matched_units else None,
                matched_units=matched_units,
            )

        return SearchResult()

    def _resolve_conversion(self, from_text: str, to_text: str) -> SearchResult:
        """Resolve a conversion query to specific units.

        Args:
            from_text: Text identifying the source unit.
            to_text: Text identifying the target unit.

        Returns:
            SearchResult with resolved units and category.
        """
        from_matches = self._search_all_units(from_text)
        to_matches = self._search_all_units(to_text)

        if not from_matches or not to_matches:
            # Return partial results
            all_matches = from_matches + to_matches
            return SearchResult(
                from_unit=from_matches[0][1] if from_matches else None,
                to_unit=to_matches[0][1] if to_matches else None,
                matched_units=all_matches,
            )

        # Find a pair where both units are in the same category
        for from_cat, from_unit in from_matches:
            for to_cat, to_unit in to_matches:
                if from_cat.id == to_cat.id:
                    return SearchResult(
                        category=from_cat,
                        from_unit=from_unit,
                        to_unit=to_unit,
                        matched_units=from_matches + to_matches,
                    )

        # No same-category match; return first results
        return SearchResult(
            category=from_matches[0][0],
            from_unit=from_matches[0][1],
            to_unit=to_matches[0][1],
            matched_units=from_matches + to_matches,
        )

    def _find_category(self, query: str) -> Optional[Category]:
        """Find a category by name (case-insensitive).

        Args:
            query: The search string.

        Returns:
            The matching Category if found.
        """
        query_lower = query.lower()
        for category in self._converter.categories:
            if category.name.lower() == query_lower:
                return category
            if category.id.lower() == query_lower:
                return category
        return None

    def _search_all_units(self, query: str) -> list[tuple[Category, Unit]]:
        """Search for matching units across all categories.

        Args:
            query: The search string.

        Returns:
            List of (Category, Unit) tuples for all matches.
        """
        results: list[tuple[Category, Unit]] = []
        query_lower = query.lower().strip()

        for category in self._converter.categories:
            for unit in category.units:
                if self._unit_matches(unit, query_lower):
                    results.append((category, unit))

        return results

    @staticmethod
    def _unit_matches(unit: Unit, query_lower: str) -> bool:
        """Check if a unit matches a query string.

        Performs case-insensitive matching against id, name, symbol,
        and aliases.

        Args:
            unit: The unit to check.
            query_lower: The lowercase search string.

        Returns:
            True if the unit matches.
        """
        if query_lower in unit.id.lower():
            return True
        if query_lower in unit.name.lower():
            return True
        if query_lower == unit.symbol.lower():
            return True
        for alias in unit.aliases:
            if query_lower in alias.lower():
                return True
        return False
