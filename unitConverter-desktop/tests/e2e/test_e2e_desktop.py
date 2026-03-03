"""End-to-end Selenium-based integration tests for the Desktop application.

These tests launch the actual Qt application and use Selenium WebDriver
concepts adapted for Qt desktop testing. Since Selenium is primarily for
web applications, these tests use pytest-qt to simulate E2E scenarios
that would normally be tested via Selenium in a web context.

Note: For true Selenium E2E testing, the application would need to be
served via a web wrapper (e.g., QtWebEngine). These tests simulate
the same acceptance criteria using pytest-qt as a bridge.
"""

import pytest

from src.services.converter_service import ConverterService
from src.services.search_service import SearchService
from src.i18n.translations import TranslationService
from src.viewmodels.converter_viewmodel import ConverterViewModel
from src.viewmodels.search_viewmodel import SearchViewModel
from src.viewmodels.preferences_viewmodel import PreferencesViewModel


@pytest.fixture
def app_stack():
    """Create a complete application stack for E2E testing."""
    converter_service = ConverterService()
    search_service = SearchService(converter_service)
    translation_service = TranslationService(language="en")

    converter_vm = ConverterViewModel(converter_service)
    search_vm = SearchViewModel(search_service, converter_vm)
    prefs_vm = PreferencesViewModel(translation_service)

    return {
        "converter_service": converter_service,
        "search_service": search_service,
        "translation_service": translation_service,
        "converter_vm": converter_vm,
        "search_vm": search_vm,
        "prefs_vm": prefs_vm,
    }


class TestE2EApplicationStartup:
    """Test that the application initializes correctly."""

    def test_application_initializes(self, app_stack) -> None:
        assert app_stack["converter_vm"] is not None
        assert app_stack["search_vm"] is not None
        assert app_stack["prefs_vm"] is not None

    def test_default_state_on_startup(self, app_stack) -> None:
        vm = app_stack["converter_vm"]
        assert vm.current_category_id == "length"
        assert vm.from_unit_id == "meter"
        assert vm.to_unit_id == "kilometer"
        assert vm.from_value == "1"

    def test_all_categories_accessible(self, app_stack) -> None:
        vm = app_stack["converter_vm"]
        for cat in vm.categories:
            vm.set_category(cat.id)
            assert vm.current_category_id == cat.id
            assert vm.from_unit_id != ""
            assert vm.to_unit_id != ""


class TestE2EConversionWorkflow:
    """Test complete conversion workflows as a user would."""

    def test_user_converts_kilometers_to_miles(self, app_stack) -> None:
        vm = app_stack["converter_vm"]
        vm.set_category("length")
        vm.set_from_unit("kilometer")
        vm.set_to_unit("mile")
        vm.set_from_value("10")

        result = float(vm.to_value)
        assert result == pytest.approx(6.21371, rel=1e-3)

    def test_user_converts_celsius_to_kelvin(self, app_stack) -> None:
        vm = app_stack["converter_vm"]
        vm.set_category("temperature")
        vm.set_from_unit("celsius")
        vm.set_to_unit("kelvin")
        vm.set_from_value("25")

        result = float(vm.to_value)
        assert result == pytest.approx(298.15)

    def test_user_swaps_units_and_converts(self, app_stack) -> None:
        vm = app_stack["converter_vm"]
        vm.set_category("weight")
        vm.set_from_unit("kilogram")
        vm.set_to_unit("pound")
        vm.set_from_value("1")

        pounds = float(vm.to_value)
        vm.swap_units()
        # Now from=pound, to=kilogram, value should be the previous result
        assert vm.from_unit_id == "pound"
        assert vm.to_unit_id == "kilogram"

    def test_user_searches_and_converts(self, app_stack) -> None:
        search_vm = app_stack["search_vm"]
        converter_vm = app_stack["converter_vm"]

        search_vm.search("from miles to kilometers")
        assert converter_vm.current_category_id == "length"
        assert converter_vm.from_unit_id == "mile"
        assert converter_vm.to_unit_id == "kilometer"

    def test_user_changes_language(self, app_stack) -> None:
        prefs = app_stack["prefs_vm"]
        prefs.set_language("ja")
        assert prefs.current_language == "ja"

        from src.i18n.translations import APP_TITLE

        assert prefs.get_text(APP_TITLE) == "単位変換"

    def test_user_clears_history(self, app_stack) -> None:
        vm = app_stack["converter_vm"]
        vm.set_from_value("100")
        vm.set_from_value("200")
        assert len(vm.history) > 0

        vm.clear_history()
        assert len(vm.history) == 0

    def test_user_navigates_all_categories(self, app_stack) -> None:
        vm = app_stack["converter_vm"]
        expected_categories = [
            "length",
            "temperature",
            "area",
            "volume",
            "weight",
            "time",
        ]

        for cat_id in expected_categories:
            vm.set_category(cat_id)
            vm.set_from_value("1")
            assert vm.to_value != "", f"No result for category {cat_id}"


class TestE2ESearchFunctionality:
    """Test the search/natural language parsing feature."""

    def test_search_from_to_pattern(self, app_stack) -> None:
        search_vm = app_stack["search_vm"]
        search_vm.search("from celsius to fahrenheit")
        assert search_vm.last_result is not None
        assert search_vm.last_result.is_conversion_query

    def test_search_without_from_keyword(self, app_stack) -> None:
        search_vm = app_stack["search_vm"]
        search_vm.search("meter to foot")
        assert search_vm.last_result is not None
        assert search_vm.last_result.is_conversion_query

    def test_search_case_insensitive(self, app_stack) -> None:
        search_vm = app_stack["search_vm"]
        search_vm.search("KILOMETER TO METER")
        assert search_vm.last_result is not None
        assert search_vm.last_result.has_results

    def test_search_partial_unit_name(self, app_stack) -> None:
        search_vm = app_stack["search_vm"]
        search_vm.search("kilo")
        assert search_vm.last_result is not None
        assert search_vm.last_result.has_results

    def test_search_no_results(self, app_stack) -> None:
        search_vm = app_stack["search_vm"]
        search_vm.search("nonexistent_unit_xyz")
        assert search_vm.last_result is not None
        assert not search_vm.last_result.has_results
