"""Unit tests for the models layer (Unit, Category, ConversionResult)."""

import pytest
from datetime import datetime

from src.models.unit import Unit
from src.models.category import Category
from src.models.conversion_result import ConversionResult


class TestUnit:
    """Tests for the Unit model."""

    def test_unit_creation(self) -> None:
        unit = Unit(id="meter", name="Meter", symbol="m", factor=1.0)
        assert unit.id == "meter"
        assert unit.name == "Meter"
        assert unit.symbol == "m"
        assert unit.factor == 1.0

    def test_unit_with_aliases(self) -> None:
        unit = Unit(
            id="kilometer",
            name="Kilometer",
            symbol="km",
            factor=1000.0,
            aliases=("kilometers", "km"),
        )
        assert len(unit.aliases) == 2
        assert "kilometers" in unit.aliases

    def test_unit_is_frozen(self) -> None:
        unit = Unit(id="meter", name="Meter", symbol="m")
        with pytest.raises(AttributeError):
            unit.id = "changed"

    def test_matches_search_by_name(self) -> None:
        unit = Unit(id="meter", name="Meter", symbol="m")
        assert unit.matches_search("Meter")
        assert unit.matches_search("meter")
        assert unit.matches_search("met")

    def test_matches_search_by_id(self) -> None:
        unit = Unit(id="kilometer", name="Kilometer", symbol="km")
        assert unit.matches_search("kilometer")

    def test_matches_search_by_symbol(self) -> None:
        unit = Unit(id="meter", name="Meter", symbol="m")
        assert unit.matches_search("m")

    def test_matches_search_by_alias(self) -> None:
        unit = Unit(
            id="foot", name="Foot", symbol="ft", factor=0.3048, aliases=("feet",)
        )
        assert unit.matches_search("feet")

    def test_matches_search_case_insensitive(self) -> None:
        unit = Unit(id="meter", name="Meter", symbol="m")
        assert unit.matches_search("METER")
        assert unit.matches_search("MeTeR")

    def test_matches_search_empty_query(self) -> None:
        unit = Unit(id="meter", name="Meter", symbol="m")
        assert unit.matches_search("")
        assert unit.matches_search("   ")

    def test_matches_search_no_match(self) -> None:
        unit = Unit(id="meter", name="Meter", symbol="m")
        assert not unit.matches_search("kilogram")

    def test_default_factor(self) -> None:
        unit = Unit(id="test", name="Test", symbol="t")
        assert unit.factor == 1.0

    def test_default_aliases(self) -> None:
        unit = Unit(id="test", name="Test", symbol="t")
        assert unit.aliases == ()


class TestCategory:
    """Tests for the Category model."""

    @pytest.fixture
    def length_category(self) -> Category:
        return Category(
            id="length",
            name="Length",
            icon="📏",
            units=(
                Unit(id="meter", name="Meter", symbol="m", factor=1.0),
                Unit(id="kilometer", name="Kilometer", symbol="km", factor=1000.0),
                Unit(id="centimeter", name="Centimeter", symbol="cm", factor=0.01),
            ),
        )

    def test_category_creation(self, length_category: Category) -> None:
        assert length_category.id == "length"
        assert length_category.name == "Length"
        assert length_category.icon == "📏"
        assert len(length_category.units) == 3

    def test_default_from_unit(self, length_category: Category) -> None:
        assert length_category.default_from_unit is not None
        assert length_category.default_from_unit.id == "meter"

    def test_default_to_unit(self, length_category: Category) -> None:
        assert length_category.default_to_unit is not None
        assert length_category.default_to_unit.id == "kilometer"

    def test_default_units_empty_category(self) -> None:
        cat = Category(id="empty", name="Empty", icon="")
        assert cat.default_from_unit is None
        assert cat.default_to_unit is None

    def test_default_to_unit_single(self) -> None:
        cat = Category(
            id="single",
            name="Single",
            icon="",
            units=(Unit(id="only", name="Only", symbol="o"),),
        )
        assert cat.default_to_unit.id == "only"

    def test_get_unit_by_id(self, length_category: Category) -> None:
        unit = length_category.get_unit_by_id("kilometer")
        assert unit is not None
        assert unit.symbol == "km"

    def test_get_unit_by_id_not_found(self, length_category: Category) -> None:
        assert length_category.get_unit_by_id("nonexistent") is None

    def test_search_units(self, length_category: Category) -> None:
        results = length_category.search_units("meter")
        assert len(results) >= 1
        assert any(u.id == "meter" for u in results)

    def test_search_units_empty_query(self, length_category: Category) -> None:
        results = length_category.search_units("")
        assert len(results) == 3


class TestConversionResult:
    """Tests for the ConversionResult model."""

    def test_creation(self) -> None:
        result = ConversionResult(
            from_value=1.0,
            to_value=1000.0,
            from_unit_symbol="km",
            to_unit_symbol="m",
            from_unit_name="Kilometer",
            to_unit_name="Meter",
            category_id="length",
        )
        assert result.from_value == 1.0
        assert result.to_value == 1000.0
        assert result.category_id == "length"

    def test_display_string(self) -> None:
        result = ConversionResult(
            from_value=5.0,
            to_value=5000.0,
            from_unit_symbol="km",
            to_unit_symbol="m",
            from_unit_name="Kilometer",
            to_unit_name="Meter",
            category_id="length",
        )
        assert "5" in result.display_string
        assert "5000" in result.display_string
        assert "km" in result.display_string
        assert "m" in result.display_string
        assert "→" in result.display_string

    def test_time_string(self) -> None:
        result = ConversionResult(
            from_value=1.0,
            to_value=1.0,
            from_unit_symbol="m",
            to_unit_symbol="m",
            from_unit_name="Meter",
            to_unit_name="Meter",
            category_id="length",
        )
        # Should be HH:MM:SS format
        assert len(result.time_string.split(":")) == 3

    def test_format_number_zero(self) -> None:
        assert ConversionResult._format_number(0) == "0"

    def test_format_number_integer(self) -> None:
        result = ConversionResult._format_number(42.0)
        assert "42" in result

    def test_format_number_decimal(self) -> None:
        result = ConversionResult._format_number(3.14159)
        assert "3.14159" in result

    def test_timestamp_auto_created(self) -> None:
        result = ConversionResult(
            from_value=1.0,
            to_value=1.0,
            from_unit_symbol="m",
            to_unit_symbol="m",
            from_unit_name="Meter",
            to_unit_name="Meter",
            category_id="length",
        )
        assert isinstance(result.timestamp, datetime)
