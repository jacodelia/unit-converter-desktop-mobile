"""ViewModel for the search functionality."""

from PySide6.QtCore import QObject, Signal, Slot

from src.services.search_service import SearchResult, SearchService
from src.viewmodels.converter_viewmodel import ConverterViewModel


class SearchViewModel(QObject):
    """ViewModel managing search state and actions.

    Provides reactive search results and can apply search results
    to the converter ViewModel.

    Signals:
        search_results_changed: Emitted when search results update.
        navigation_triggered: Emitted when a search navigates to a unit.
    """

    search_results_changed = Signal(object)
    navigation_triggered = Signal(str, str, str)  # category_id, from_id, to_id

    def __init__(
        self,
        search_service: SearchService,
        converter_viewmodel: ConverterViewModel,
    ) -> None:
        """Initialize with search and converter services.

        Args:
            search_service: The search parsing service.
            converter_viewmodel: The converter ViewModel to update.
        """
        super().__init__()
        self._search_service = search_service
        self._converter_vm = converter_viewmodel
        self._last_result: SearchResult | None = None
        self._query: str = ""

    @property
    def query(self) -> str:
        """Return the current search query."""
        return self._query

    @property
    def last_result(self) -> SearchResult | None:
        """Return the most recent search result."""
        return self._last_result

    @Slot(str)
    def search(self, query: str) -> None:
        """Perform a search and emit results.

        Args:
            query: The search string.
        """
        self._query = query
        if not query.strip():
            self._last_result = None
            self.search_results_changed.emit(None)
            return

        result = self._search_service.search(query)
        self._last_result = result
        self.search_results_changed.emit(result)

        # If it's a complete conversion query, navigate automatically
        if result.is_conversion_query and result.category:
            self._apply_search_result(result)

    def apply_result(self) -> None:
        """Apply the last search result to the converter."""
        if self._last_result and self._last_result.has_results:
            self._apply_search_result(self._last_result)

    def _apply_search_result(self, result: SearchResult) -> None:
        """Apply a search result to the converter ViewModel.

        Args:
            result: The search result to apply.
        """
        if result.category and result.from_unit and result.to_unit:
            self._converter_vm.set_units_from_search(
                result.category.id,
                result.from_unit.id,
                result.to_unit.id,
            )
            self.navigation_triggered.emit(
                result.category.id,
                result.from_unit.id,
                result.to_unit.id,
            )
        elif result.category and result.from_unit:
            # Navigate to category with the matched unit as "from"
            category = result.category
            to_unit = category.default_to_unit
            if to_unit and to_unit.id == result.from_unit.id:
                to_unit = category.default_from_unit
            to_id = to_unit.id if to_unit else result.from_unit.id
            self._converter_vm.set_units_from_search(
                category.id,
                result.from_unit.id,
                to_id,
            )
            self.navigation_triggered.emit(
                category.id,
                result.from_unit.id,
                to_id,
            )
        elif result.category:
            self._converter_vm.set_category(result.category.id)
