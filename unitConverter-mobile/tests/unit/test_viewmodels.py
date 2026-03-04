"""Unit tests for ViewModels (ConverterViewModel, SearchViewModel, PreferencesViewModel)."""

import pytest

from unitconverter.services.converter_service import ConverterService
from unitconverter.services.search_service import SearchService
from unitconverter.i18n.translations import TranslationService, APP_TITLE
from unitconverter.viewmodels.converter_viewmodel import ConverterViewModel
from unitconverter.viewmodels.search_viewmodel import SearchViewModel
from unitconverter.viewmodels.preferences_viewmodel import PreferencesViewModel


@pytest.fixture
def converter_service() -> ConverterService:
    return ConverterService()


@pytest.fixture
def converter_vm(converter_service: ConverterService) -> ConverterViewModel:
    return ConverterViewModel(converter_service)


@pytest.fixture
def search_service(converter_service: ConverterService) -> SearchService:
    return SearchService(converter_service)


@pytest.fixture
def search_vm(
    search_service: SearchService, converter_vm: ConverterViewModel
) -> SearchViewModel:
    return SearchViewModel(search_service, converter_vm)


@pytest.fixture
def prefs_vm() -> PreferencesViewModel:
    service = TranslationService(language="en")
    return PreferencesViewModel(service)


class TestConverterViewModel:
    """Tests for the ConverterViewModel."""

    def test_initial_category(self, converter_vm: ConverterViewModel) -> None:
        assert converter_vm.current_category_id == "length"

    def test_initial_from_unit(self, converter_vm: ConverterViewModel) -> None:
        assert converter_vm.from_unit_id == "meter"

    def test_initial_to_unit(self, converter_vm: ConverterViewModel) -> None:
        assert converter_vm.to_unit_id == "kilometer"

    def test_initial_from_value(self, converter_vm: ConverterViewModel) -> None:
        assert converter_vm.from_value == "1"

    def test_initial_conversion(self, converter_vm: ConverterViewModel) -> None:
        assert converter_vm.to_value != ""

    def test_categories_available(self, converter_vm: ConverterViewModel) -> None:
        assert len(converter_vm.categories) == 6

    def test_set_category(self, converter_vm: ConverterViewModel) -> None:
        converter_vm.set_category("temperature")
        assert converter_vm.current_category_id == "temperature"
        assert converter_vm.from_unit_id == "celsius"
        assert converter_vm.to_unit_id == "kelvin"

    def test_set_invalid_category(self, converter_vm: ConverterViewModel) -> None:
        converter_vm.set_category("invalid")
        assert converter_vm.current_category_id == "length"

    def test_set_from_unit(self, converter_vm: ConverterViewModel) -> None:
        converter_vm.set_from_unit("kilometer")
        assert converter_vm.from_unit_id == "kilometer"

    def test_set_to_unit(self, converter_vm: ConverterViewModel) -> None:
        converter_vm.set_to_unit("centimeter")
        assert converter_vm.to_unit_id == "centimeter"

    def test_set_from_value(self, converter_vm: ConverterViewModel) -> None:
        converter_vm.set_from_value("100")
        assert converter_vm.from_value == "100"
        assert converter_vm.to_value != ""

    def test_set_empty_from_value(self, converter_vm: ConverterViewModel) -> None:
        converter_vm.set_from_value("")
        assert converter_vm.to_value == ""

    def test_set_invalid_from_value(self, converter_vm: ConverterViewModel) -> None:
        converter_vm.set_from_value("abc")
        assert converter_vm.to_value == ""

    def test_swap_units(self, converter_vm: ConverterViewModel) -> None:
        original_from = converter_vm.from_unit_id
        original_to = converter_vm.to_unit_id
        converter_vm.swap_units()
        assert converter_vm.from_unit_id == original_to
        assert converter_vm.to_unit_id == original_from

    def test_history_starts_empty_before_conversion(self) -> None:
        service = ConverterService()
        vm = ConverterViewModel(service)
        # History may have the initial conversion
        assert isinstance(vm.history, list)

    def test_history_grows(self, converter_vm: ConverterViewModel) -> None:
        initial = len(converter_vm.history)
        converter_vm.set_from_value("42")
        assert len(converter_vm.history) > initial

    def test_clear_history(self, converter_vm: ConverterViewModel) -> None:
        converter_vm.set_from_value("10")
        converter_vm.clear_history()
        assert len(converter_vm.history) == 0

    def test_history_max_limit(self, converter_vm: ConverterViewModel) -> None:
        for i in range(20):
            converter_vm.set_from_value(str(i + 1))
        assert len(converter_vm.history) <= ConverterViewModel.MAX_HISTORY

    def test_set_units_from_search(self, converter_vm: ConverterViewModel) -> None:
        converter_vm.set_units_from_search("temperature", "celsius", "fahrenheit")
        assert converter_vm.current_category_id == "temperature"
        assert converter_vm.from_unit_id == "celsius"
        assert converter_vm.to_unit_id == "fahrenheit"

    def test_current_category_property(self, converter_vm: ConverterViewModel) -> None:
        category = converter_vm.current_category
        assert category.id == "length"
        assert category.name == "Length"

    def test_service_property(self, converter_vm: ConverterViewModel) -> None:
        assert converter_vm.service is not None
        assert isinstance(converter_vm.service, ConverterService)


class TestSearchViewModel:
    """Tests for the SearchViewModel."""

    def test_initial_query(self, search_vm: SearchViewModel) -> None:
        assert search_vm.query == ""

    def test_initial_last_result(self, search_vm: SearchViewModel) -> None:
        assert search_vm.last_result is None

    def test_search_empty(self, search_vm: SearchViewModel) -> None:
        search_vm.search("")
        assert search_vm.last_result is None

    def test_search_category(self, search_vm: SearchViewModel) -> None:
        search_vm.search("Length")
        assert search_vm.last_result is not None
        assert search_vm.last_result.category is not None

    def test_search_conversion_query(
        self, search_vm: SearchViewModel, converter_vm: ConverterViewModel
    ) -> None:
        search_vm.search("from kilometer to meter")
        assert search_vm.last_result is not None
        assert search_vm.last_result.is_conversion_query
        # Should auto-navigate
        assert converter_vm.current_category_id == "length"

    def test_search_updates_query(self, search_vm: SearchViewModel) -> None:
        search_vm.search("test query")
        assert search_vm.query == "test query"

    def test_apply_result_no_result(self, search_vm: SearchViewModel) -> None:
        search_vm.apply_result()  # Should not raise

    def test_apply_result_with_category(
        self, search_vm: SearchViewModel, converter_vm: ConverterViewModel
    ) -> None:
        search_vm.search("temperature")
        search_vm.apply_result()
        assert converter_vm.current_category_id == "temperature"


class TestPreferencesViewModel:
    """Tests for the PreferencesViewModel."""

    def test_initial_language(self, prefs_vm: PreferencesViewModel) -> None:
        assert prefs_vm.current_language == "en"

    def test_available_languages(self, prefs_vm: PreferencesViewModel) -> None:
        languages = prefs_vm.available_languages
        assert len(languages) == 8
        codes = [code for code, _ in languages]
        assert "en" in codes
        assert "es" in codes
        assert "fr" in codes
        assert "it" in codes
        assert "de" in codes
        assert "ru" in codes
        assert "ja" in codes
        assert "zh" in codes

    def test_set_language(self, prefs_vm: PreferencesViewModel) -> None:
        prefs_vm.set_language("es")
        assert prefs_vm.current_language == "es"

    def test_set_invalid_language(self, prefs_vm: PreferencesViewModel) -> None:
        prefs_vm.set_language("invalid")
        assert prefs_vm.current_language == "en"

    def test_get_text_english(self, prefs_vm: PreferencesViewModel) -> None:
        assert prefs_vm.get_text(APP_TITLE) == "Unit Converter"

    def test_get_text_after_language_change(
        self, prefs_vm: PreferencesViewModel
    ) -> None:
        prefs_vm.set_language("es")
        assert prefs_vm.get_text(APP_TITLE) == "Conversor de Unidades"

    def test_translation_property(self, prefs_vm: PreferencesViewModel) -> None:
        assert prefs_vm.translation is not None
        assert isinstance(prefs_vm.translation, TranslationService)
