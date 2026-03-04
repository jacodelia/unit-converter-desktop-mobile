"""ViewModel for the main converter functionality.

Implements the MVVM pattern by exposing reactive properties via events
and providing commands that the View can bind to.
"""

from unitconverter.models.category import Category
from unitconverter.models.conversion_result import ConversionResult
from unitconverter.models.unit import Unit
from unitconverter.services.converter_service import ConverterService
from unitconverter.viewmodels.event_mixin import EventMixin


class ConverterViewModel(EventMixin):
    """ViewModel managing conversion state and logic.

    Events:
        category_changed(str): Emitted when the active category changes.
        from_unit_changed(str): Emitted when the source unit changes.
        to_unit_changed(str): Emitted when the target unit changes.
        result_changed(str): Emitted when the conversion result updates.
        history_changed(): Emitted when the conversion history updates.
    """

    MAX_HISTORY = 10

    def __init__(self, converter_service: ConverterService) -> None:
        """Initialize the ViewModel with a converter service.

        Args:
            converter_service: The service handling conversions.
        """
        super().__init__()
        self._service = converter_service
        self._current_category_id: str = "length"
        self._from_unit_id: str = "meter"
        self._to_unit_id: str = "kilometer"
        self._from_value: str = "1"
        self._to_value: str = ""
        self._history: list[ConversionResult] = []

        self._perform_conversion()

    @property
    def service(self) -> ConverterService:
        """Return the converter service."""
        return self._service

    @property
    def categories(self) -> tuple[Category, ...]:
        """Return all available categories."""
        return self._service.categories

    @property
    def current_category(self) -> Category:
        """Return the currently selected category."""
        cat = self._service.get_category(self._current_category_id)
        assert cat is not None
        return cat

    @property
    def current_category_id(self) -> str:
        """Return the current category ID."""
        return self._current_category_id

    @property
    def from_unit_id(self) -> str:
        """Return the current source unit ID."""
        return self._from_unit_id

    @property
    def to_unit_id(self) -> str:
        """Return the current target unit ID."""
        return self._to_unit_id

    @property
    def from_value(self) -> str:
        """Return the current input value string."""
        return self._from_value

    @property
    def to_value(self) -> str:
        """Return the current output value string."""
        return self._to_value

    @property
    def history(self) -> list[ConversionResult]:
        """Return the conversion history."""
        return list(self._history)

    def set_category(self, category_id: str) -> None:
        """Change the active category and reset units to defaults.

        Args:
            category_id: The ID of the new category.
        """
        category = self._service.get_category(category_id)
        if category is None:
            return

        self._current_category_id = category_id
        default_from = category.default_from_unit
        default_to = category.default_to_unit

        self._from_unit_id = default_from.id if default_from else ""
        self._to_unit_id = default_to.id if default_to else ""

        self.emit("category_changed", category_id)
        self._perform_conversion()

    def set_from_unit(self, unit_id: str) -> None:
        """Change the source unit.

        Args:
            unit_id: The ID of the new source unit.
        """
        self._from_unit_id = unit_id
        self.emit("from_unit_changed", unit_id)
        self._perform_conversion()

    def set_to_unit(self, unit_id: str) -> None:
        """Change the target unit.

        Args:
            unit_id: The ID of the new target unit.
        """
        self._to_unit_id = unit_id
        self.emit("to_unit_changed", unit_id)
        self._perform_conversion()

    def set_from_value(self, value: str) -> None:
        """Update the input value and recalculate.

        Args:
            value: The new input value as a string.
        """
        self._from_value = value
        self._perform_conversion()

    def swap_units(self) -> None:
        """Swap the source and target units."""
        self._from_unit_id, self._to_unit_id = (
            self._to_unit_id,
            self._from_unit_id,
        )
        self._from_value = self._to_value
        self.emit("from_unit_changed", self._from_unit_id)
        self.emit("to_unit_changed", self._to_unit_id)
        self._perform_conversion()

    def clear_history(self) -> None:
        """Clear all conversion history."""
        self._history.clear()
        self.emit("history_changed")

    def set_units_from_search(
        self, category_id: str, from_unit_id: str, to_unit_id: str
    ) -> None:
        """Set category and units from a search result.

        Args:
            category_id: The category ID.
            from_unit_id: The source unit ID.
            to_unit_id: The target unit ID.
        """
        self._current_category_id = category_id
        self._from_unit_id = from_unit_id
        self._to_unit_id = to_unit_id
        self.emit("category_changed", category_id)
        self.emit("from_unit_changed", from_unit_id)
        self.emit("to_unit_changed", to_unit_id)
        self._perform_conversion()

    def _perform_conversion(self) -> None:
        """Execute the conversion and update the result."""
        if not self._from_value:
            self._to_value = ""
            self.emit("result_changed", "")
            return

        try:
            value = float(self._from_value)
        except ValueError:
            self._to_value = ""
            self.emit("result_changed", "")
            return

        try:
            result = self._service.convert(
                value,
                self._current_category_id,
                self._from_unit_id,
                self._to_unit_id,
            )
            self._to_value = ConversionResult._format_number(result.to_value)
            self.emit("result_changed", self._to_value)

            # Add to history
            self._history.insert(0, result)
            if len(self._history) > self.MAX_HISTORY:
                self._history = self._history[: self.MAX_HISTORY]
            self.emit("history_changed")

        except (ValueError, ZeroDivisionError):
            self._to_value = ""
            self.emit("result_changed", "")
