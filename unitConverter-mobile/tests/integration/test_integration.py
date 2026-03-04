"""Integration tests that verify end-to-end workflows across layers."""

import pytest

from unitconverter.services.converter_service import ConverterService
from unitconverter.services.search_service import SearchService
from unitconverter.i18n.translations import TranslationService
from unitconverter.viewmodels.converter_viewmodel import ConverterViewModel
from unitconverter.viewmodels.search_viewmodel import SearchViewModel
from unitconverter.viewmodels.preferences_viewmodel import PreferencesViewModel


@pytest.fixture
def full_stack():
    """Create a complete stack of services and ViewModels."""
    converter_service = ConverterService()
    search_service = SearchService(converter_service)
    translation_service = TranslationService(language="en")

    converter_vm = ConverterViewModel(converter_service)
    search_vm = SearchViewModel(search_service, converter_vm)
    prefs_vm = PreferencesViewModel(translation_service)

    return converter_vm, search_vm, prefs_vm


class TestEndToEndConversion:
    """Test complete conversion workflows."""

    def test_length_conversion_flow(self, full_stack) -> None:
        converter_vm, _, _ = full_stack
        converter_vm.set_category("length")
        converter_vm.set_from_unit("kilometer")
        converter_vm.set_to_unit("meter")
        converter_vm.set_from_value("5")
        assert converter_vm.to_value != ""
        assert float(converter_vm.to_value) == pytest.approx(5000.0)

    def test_temperature_conversion_flow(self, full_stack) -> None:
        converter_vm, _, _ = full_stack
        converter_vm.set_category("temperature")
        converter_vm.set_from_unit("celsius")
        converter_vm.set_to_unit("fahrenheit")
        converter_vm.set_from_value("100")
        assert float(converter_vm.to_value) == pytest.approx(212.0)

    def test_search_and_convert_flow(self, full_stack) -> None:
        converter_vm, search_vm, _ = full_stack
        search_vm.search("from kilometer to meter")
        assert converter_vm.current_category_id == "length"
        assert converter_vm.from_unit_id == "kilometer"
        assert converter_vm.to_unit_id == "meter"

    def test_swap_and_convert_flow(self, full_stack) -> None:
        converter_vm, _, _ = full_stack
        converter_vm.set_category("length")
        converter_vm.set_from_unit("meter")
        converter_vm.set_to_unit("kilometer")
        converter_vm.set_from_value("1000")

        original_result = converter_vm.to_value
        converter_vm.swap_units()
        # After swap, from=kilometer, to=meter
        assert converter_vm.from_unit_id == "kilometer"
        assert converter_vm.to_unit_id == "meter"

    def test_language_change_flow(self, full_stack) -> None:
        _, _, prefs_vm = full_stack
        prefs_vm.set_language("es")
        assert prefs_vm.current_language == "es"
        from unitconverter.i18n.translations import APP_TITLE

        assert prefs_vm.get_text(APP_TITLE) == "Conversor de Unidades"

    def test_history_accumulation_flow(self, full_stack) -> None:
        converter_vm, _, _ = full_stack
        converter_vm.clear_history()
        converter_vm.set_from_value("10")
        converter_vm.set_from_value("20")
        converter_vm.set_from_value("30")
        assert len(converter_vm.history) >= 3

    def test_category_switch_resets_units(self, full_stack) -> None:
        converter_vm, _, _ = full_stack
        converter_vm.set_category("weight")
        assert converter_vm.from_unit_id == "kilogram"
        assert converter_vm.to_unit_id == "gram"

        converter_vm.set_category("time")
        assert converter_vm.from_unit_id == "second"
        assert converter_vm.to_unit_id == "millisecond"

    def test_all_categories_convertible(self, full_stack) -> None:
        converter_vm, _, _ = full_stack
        for category in converter_vm.categories:
            converter_vm.set_category(category.id)
            converter_vm.set_from_value("1")
            assert converter_vm.to_value != "", (
                f"Conversion failed for category: {category.id}"
            )

    def test_search_navigates_to_correct_category(self, full_stack) -> None:
        converter_vm, search_vm, _ = full_stack
        search_vm.search("celsius to fahrenheit")
        assert converter_vm.current_category_id == "temperature"

    def test_all_languages_produce_text(self, full_stack) -> None:
        _, _, prefs_vm = full_stack
        from unitconverter.i18n.translations import APP_TITLE, SUPPORTED_LANGUAGES

        for lang in SUPPORTED_LANGUAGES:
            prefs_vm.set_language(lang)
            text = prefs_vm.get_text(APP_TITLE)
            assert len(text) > 0, f"Empty text for language: {lang}"

    def test_large_value_conversion(self, full_stack) -> None:
        converter_vm, _, _ = full_stack
        converter_vm.set_category("length")
        converter_vm.set_from_unit("lightyear")
        converter_vm.set_to_unit("meter")
        converter_vm.set_from_value("1")
        assert converter_vm.to_value != ""
        assert float(converter_vm.to_value) > 0

    def test_very_small_value_conversion(self, full_stack) -> None:
        converter_vm, _, _ = full_stack
        converter_vm.set_category("weight")
        converter_vm.set_from_unit("amu")
        converter_vm.set_to_unit("kilogram")
        converter_vm.set_from_value("1")
        assert converter_vm.to_value != ""

    def test_negative_temperature_conversion(self, full_stack) -> None:
        converter_vm, _, _ = full_stack
        converter_vm.set_category("temperature")
        converter_vm.set_from_unit("celsius")
        converter_vm.set_to_unit("kelvin")
        converter_vm.set_from_value("-273.15")
        assert float(converter_vm.to_value) == pytest.approx(0.0, abs=0.01)
