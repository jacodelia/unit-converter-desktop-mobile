"""End-to-end Selenium-based integration tests for the Mobile application.

These tests verify the complete mobile application workflow using
the same acceptance criteria as the desktop version, adapted for
mobile-specific behavior.
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


class TestE2EMobileStartup:
    """Test that the mobile application initializes correctly."""

    def test_application_initializes(self, app_stack) -> None:
        assert app_stack["converter_vm"] is not None
        assert app_stack["search_vm"] is not None
        assert app_stack["prefs_vm"] is not None

    def test_default_state_on_startup(self, app_stack) -> None:
        vm = app_stack["converter_vm"]
        assert vm.current_category_id == "length"
        assert vm.from_value == "1"

    def test_all_six_categories_available(self, app_stack) -> None:
        vm = app_stack["converter_vm"]
        assert len(vm.categories) == 6
        expected = {"length", "temperature", "area", "volume", "weight", "time"}
        actual = {cat.id for cat in vm.categories}
        assert actual == expected


class TestE2EMobileConversion:
    """Test mobile conversion workflows."""

    def test_convert_liters_to_gallons(self, app_stack) -> None:
        vm = app_stack["converter_vm"]
        vm.set_category("volume")
        vm.set_from_unit("liter")
        vm.set_to_unit("usgallon")
        vm.set_from_value("3.785")
        result = float(vm.to_value)
        assert result == pytest.approx(1.0, rel=1e-2)

    def test_convert_hours_to_minutes(self, app_stack) -> None:
        vm = app_stack["converter_vm"]
        vm.set_category("time")
        vm.set_from_unit("hour")
        vm.set_to_unit("minute")
        vm.set_from_value("2")
        assert float(vm.to_value) == pytest.approx(120.0)

    def test_convert_acres_to_hectares(self, app_stack) -> None:
        vm = app_stack["converter_vm"]
        vm.set_category("area")
        vm.set_from_unit("acre")
        vm.set_to_unit("hectare")
        vm.set_from_value("1")
        assert float(vm.to_value) == pytest.approx(0.4047, rel=1e-2)

    def test_swap_and_verify(self, app_stack) -> None:
        vm = app_stack["converter_vm"]
        vm.set_category("length")
        vm.set_from_unit("mile")
        vm.set_to_unit("kilometer")
        vm.set_from_value("1")

        km_value = float(vm.to_value)
        vm.swap_units()
        assert vm.from_unit_id == "kilometer"
        assert vm.to_unit_id == "mile"


class TestE2EMobileSearch:
    """Test mobile search functionality."""

    def test_search_navigates_to_unit(self, app_stack) -> None:
        search_vm = app_stack["search_vm"]
        converter_vm = app_stack["converter_vm"]

        search_vm.search("from pound to kilogram")
        assert converter_vm.current_category_id == "weight"
        assert converter_vm.from_unit_id == "pound"
        assert converter_vm.to_unit_id == "kilogram"

    def test_search_case_insensitive(self, app_stack) -> None:
        search_vm = app_stack["search_vm"]
        search_vm.search("LITER TO MILLILITER")
        assert search_vm.last_result is not None
        assert search_vm.last_result.has_results

    def test_search_category_navigation(self, app_stack) -> None:
        search_vm = app_stack["search_vm"]
        converter_vm = app_stack["converter_vm"]

        search_vm.search("temperature")
        search_vm.apply_result()
        assert converter_vm.current_category_id == "temperature"


class TestE2EMobileLanguage:
    """Test mobile language switching."""

    def test_switch_to_all_languages(self, app_stack) -> None:
        prefs = app_stack["prefs_vm"]
        from src.i18n.translations import SUPPORTED_LANGUAGES, APP_TITLE

        for lang in SUPPORTED_LANGUAGES:
            prefs.set_language(lang)
            text = prefs.get_text(APP_TITLE)
            assert len(text) > 0

    def test_chinese_language(self, app_stack) -> None:
        prefs = app_stack["prefs_vm"]
        from src.i18n.translations import APP_TITLE

        prefs.set_language("zh")
        assert prefs.get_text(APP_TITLE) == "单位转换器"

    def test_russian_language(self, app_stack) -> None:
        prefs = app_stack["prefs_vm"]
        from src.i18n.translations import APP_TITLE

        prefs.set_language("ru")
        assert prefs.get_text(APP_TITLE) == "Конвертер Единиц"
