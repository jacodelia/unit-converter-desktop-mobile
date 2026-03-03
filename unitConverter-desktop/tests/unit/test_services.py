"""Unit tests for the service layer (ConverterService, SearchService)."""

import pytest

from src.services.converter_service import ConverterService
from src.services.search_service import SearchService, SearchResult


class TestConverterService:
    """Tests for the ConverterService."""

    @pytest.fixture
    def service(self) -> ConverterService:
        return ConverterService()

    def test_categories_not_empty(self, service: ConverterService) -> None:
        assert len(service.categories) == 6

    def test_get_category_length(self, service: ConverterService) -> None:
        cat = service.get_category("length")
        assert cat is not None
        assert cat.name == "Length"

    def test_get_category_temperature(self, service: ConverterService) -> None:
        cat = service.get_category("temperature")
        assert cat is not None
        assert cat.name == "Temperature"

    def test_get_category_area(self, service: ConverterService) -> None:
        cat = service.get_category("area")
        assert cat is not None

    def test_get_category_volume(self, service: ConverterService) -> None:
        cat = service.get_category("volume")
        assert cat is not None

    def test_get_category_weight(self, service: ConverterService) -> None:
        cat = service.get_category("weight")
        assert cat is not None

    def test_get_category_time(self, service: ConverterService) -> None:
        cat = service.get_category("time")
        assert cat is not None

    def test_get_category_invalid(self, service: ConverterService) -> None:
        assert service.get_category("invalid") is None

    def test_convert_length(self, service: ConverterService) -> None:
        result = service.convert(1.0, "length", "kilometer", "meter")
        assert result.to_value == pytest.approx(1000.0)
        assert result.from_unit_symbol == "km"
        assert result.to_unit_symbol == "m"

    def test_convert_temperature(self, service: ConverterService) -> None:
        result = service.convert(100.0, "temperature", "celsius", "fahrenheit")
        assert result.to_value == pytest.approx(212.0)

    def test_convert_area(self, service: ConverterService) -> None:
        result = service.convert(1.0, "area", "hectare", "sqmeter")
        assert result.to_value == pytest.approx(10000.0)

    def test_convert_volume(self, service: ConverterService) -> None:
        result = service.convert(1.0, "volume", "liter", "milliliter")
        assert result.to_value == pytest.approx(1000.0)

    def test_convert_weight(self, service: ConverterService) -> None:
        result = service.convert(1.0, "weight", "kilogram", "gram")
        assert result.to_value == pytest.approx(1000.0)

    def test_convert_time(self, service: ConverterService) -> None:
        result = service.convert(1.0, "time", "hour", "minute")
        assert result.to_value == pytest.approx(60.0)

    def test_convert_invalid_category(self, service: ConverterService) -> None:
        with pytest.raises(ValueError, match="Unknown category"):
            service.convert(1.0, "invalid", "meter", "kilometer")

    def test_convert_invalid_from_unit(self, service: ConverterService) -> None:
        with pytest.raises(ValueError, match="Unknown unit"):
            service.convert(1.0, "length", "invalid", "meter")

    def test_convert_invalid_to_unit(self, service: ConverterService) -> None:
        with pytest.raises(ValueError, match="Unknown unit"):
            service.convert(1.0, "length", "meter", "invalid")

    def test_convert_result_has_category_id(self, service: ConverterService) -> None:
        result = service.convert(1.0, "length", "meter", "kilometer")
        assert result.category_id == "length"

    def test_convert_result_has_unit_names(self, service: ConverterService) -> None:
        result = service.convert(1.0, "length", "meter", "kilometer")
        assert result.from_unit_name == "Meter"
        assert result.to_unit_name == "Kilometer"


class TestSearchService:
    """Tests for the SearchService."""

    @pytest.fixture
    def search_service(self) -> SearchService:
        converter = ConverterService()
        return SearchService(converter)

    def test_empty_query(self, search_service: SearchService) -> None:
        result = search_service.search("")
        assert not result.has_results

    def test_whitespace_query(self, search_service: SearchService) -> None:
        result = search_service.search("   ")
        assert not result.has_results

    def test_search_category_name(self, search_service: SearchService) -> None:
        result = search_service.search("Length")
        assert result.category is not None
        assert result.category.id == "length"

    def test_search_category_case_insensitive(
        self, search_service: SearchService
    ) -> None:
        result = search_service.search("length")
        assert result.category is not None
        assert result.category.id == "length"

    def test_search_unit_name(self, search_service: SearchService) -> None:
        result = search_service.search("kilometer")
        assert result.has_results
        assert result.from_unit is not None
        assert result.from_unit.id == "kilometer"

    def test_search_conversion_query(self, search_service: SearchService) -> None:
        result = search_service.search("from kilometers to meters")
        assert result.is_conversion_query
        assert result.category is not None
        assert result.category.id == "length"
        assert result.from_unit.id == "kilometer"
        assert result.to_unit.id == "meter"

    def test_search_conversion_without_from(
        self, search_service: SearchService
    ) -> None:
        result = search_service.search("kilometer to meter")
        assert result.is_conversion_query
        assert result.from_unit.id == "kilometer"
        assert result.to_unit.id == "meter"

    def test_search_conversion_symbols(self, search_service: SearchService) -> None:
        result = search_service.search("km to m")
        assert result.has_results

    def test_search_no_results(self, search_service: SearchService) -> None:
        result = search_service.search("xyzabc123")
        assert not result.has_results

    def test_search_temperature_units(self, search_service: SearchService) -> None:
        result = search_service.search("celsius to fahrenheit")
        assert result.is_conversion_query
        assert result.category.id == "temperature"

    def test_search_weight_units(self, search_service: SearchService) -> None:
        result = search_service.search("kilogram to pound")
        assert result.is_conversion_query
        assert result.category.id == "weight"

    def test_search_result_is_conversion_query(self) -> None:
        result = SearchResult()
        assert not result.is_conversion_query

    def test_search_result_has_results_with_category(self) -> None:
        from src.models.category import Category

        result = SearchResult(category=Category(id="test", name="Test", icon=""))
        assert result.has_results

    def test_search_result_has_results_with_unit(self) -> None:
        from src.models.unit import Unit

        result = SearchResult(from_unit=Unit(id="t", name="T", symbol="t"))
        assert result.has_results

    def test_search_partial_match(self, search_service: SearchService) -> None:
        result = search_service.search("met")
        assert result.has_results
        assert result.from_unit is not None

    def test_search_alias_match(self, search_service: SearchService) -> None:
        result = search_service.search("feet")
        assert result.has_results
