"""Unit tests for all conversion operations (one per category)."""

import pytest
import math

from unitconverter.operations.length_operations import convert_length, LENGTH_UNITS
from unitconverter.operations.temperature_operations import convert_temperature, TEMPERATURE_UNITS
from unitconverter.operations.area_operations import convert_area, AREA_UNITS
from unitconverter.operations.volume_operations import convert_volume, VOLUME_UNITS
from unitconverter.operations.weight_operations import convert_weight, WEIGHT_UNITS
from unitconverter.operations.time_operations import convert_time, TIME_UNITS


class TestLengthOperations:
    """Tests for length conversion operations."""

    def test_meter_to_kilometer(self) -> None:
        result = convert_length(1000.0, "meter", "kilometer")
        assert result == pytest.approx(1.0)

    def test_kilometer_to_meter(self) -> None:
        result = convert_length(1.0, "kilometer", "meter")
        assert result == pytest.approx(1000.0)

    def test_meter_to_centimeter(self) -> None:
        result = convert_length(1.0, "meter", "centimeter")
        assert result == pytest.approx(100.0)

    def test_mile_to_kilometer(self) -> None:
        result = convert_length(1.0, "mile", "kilometer")
        assert result == pytest.approx(1.609344)

    def test_foot_to_inch(self) -> None:
        result = convert_length(1.0, "foot", "inch")
        assert result == pytest.approx(12.0)

    def test_yard_to_foot(self) -> None:
        result = convert_length(1.0, "yard", "foot")
        assert result == pytest.approx(3.0)

    def test_same_unit(self) -> None:
        result = convert_length(42.0, "meter", "meter")
        assert result == pytest.approx(42.0)

    def test_zero_value(self) -> None:
        result = convert_length(0.0, "meter", "kilometer")
        assert result == pytest.approx(0.0)

    def test_negative_value(self) -> None:
        result = convert_length(-5.0, "kilometer", "meter")
        assert result == pytest.approx(-5000.0)

    def test_micrometer_to_nanometer(self) -> None:
        result = convert_length(1.0, "micrometer", "nanometer")
        assert result == pytest.approx(1000.0)

    def test_lightyear_to_kilometer(self) -> None:
        result = convert_length(1.0, "lightyear", "kilometer")
        assert result == pytest.approx(9.461e12, rel=1e-3)

    def test_invalid_from_unit(self) -> None:
        with pytest.raises(ValueError, match="Unknown length unit"):
            convert_length(1.0, "invalid", "meter")

    def test_invalid_to_unit(self) -> None:
        with pytest.raises(ValueError, match="Unknown length unit"):
            convert_length(1.0, "meter", "invalid")

    def test_all_units_defined(self) -> None:
        expected_ids = {
            "meter",
            "kilometer",
            "centimeter",
            "millimeter",
            "micrometer",
            "nanometer",
            "mile",
            "yard",
            "foot",
            "inch",
            "lightyear",
        }
        actual_ids = {u.id for u in LENGTH_UNITS}
        assert actual_ids == expected_ids

    def test_millimeter_to_meter(self) -> None:
        result = convert_length(1000.0, "millimeter", "meter")
        assert result == pytest.approx(1.0)

    def test_inch_to_centimeter(self) -> None:
        result = convert_length(1.0, "inch", "centimeter")
        assert result == pytest.approx(2.54)


class TestTemperatureOperations:
    """Tests for temperature conversion operations."""

    def test_celsius_to_fahrenheit(self) -> None:
        result = convert_temperature(0.0, "celsius", "fahrenheit")
        assert result == pytest.approx(32.0)

    def test_celsius_to_fahrenheit_100(self) -> None:
        result = convert_temperature(100.0, "celsius", "fahrenheit")
        assert result == pytest.approx(212.0)

    def test_fahrenheit_to_celsius(self) -> None:
        result = convert_temperature(32.0, "fahrenheit", "celsius")
        assert result == pytest.approx(0.0)

    def test_celsius_to_kelvin(self) -> None:
        result = convert_temperature(0.0, "celsius", "kelvin")
        assert result == pytest.approx(273.15)

    def test_kelvin_to_celsius(self) -> None:
        result = convert_temperature(273.15, "kelvin", "celsius")
        assert result == pytest.approx(0.0)

    def test_fahrenheit_to_kelvin(self) -> None:
        result = convert_temperature(32.0, "fahrenheit", "kelvin")
        assert result == pytest.approx(273.15)

    def test_kelvin_to_fahrenheit(self) -> None:
        result = convert_temperature(273.15, "kelvin", "fahrenheit")
        assert result == pytest.approx(32.0)

    def test_same_unit(self) -> None:
        result = convert_temperature(25.0, "celsius", "celsius")
        assert result == pytest.approx(25.0)

    def test_negative_celsius(self) -> None:
        result = convert_temperature(-40.0, "celsius", "fahrenheit")
        assert result == pytest.approx(-40.0)

    def test_absolute_zero_kelvin(self) -> None:
        result = convert_temperature(0.0, "kelvin", "celsius")
        assert result == pytest.approx(-273.15)

    def test_invalid_unit(self) -> None:
        with pytest.raises(ValueError, match="Unknown temperature unit"):
            convert_temperature(1.0, "invalid", "celsius")

    def test_all_units_defined(self) -> None:
        expected_ids = {"celsius", "kelvin", "fahrenheit"}
        actual_ids = {u.id for u in TEMPERATURE_UNITS}
        assert actual_ids == expected_ids

    def test_body_temperature(self) -> None:
        result = convert_temperature(37.0, "celsius", "fahrenheit")
        assert result == pytest.approx(98.6)


class TestAreaOperations:
    """Tests for area conversion operations."""

    def test_sqmeter_to_sqkilometer(self) -> None:
        result = convert_area(1e6, "sqmeter", "sqkilometer")
        assert result == pytest.approx(1.0)

    def test_sqkilometer_to_sqmeter(self) -> None:
        result = convert_area(1.0, "sqkilometer", "sqmeter")
        assert result == pytest.approx(1e6)

    def test_hectare_to_sqmeter(self) -> None:
        result = convert_area(1.0, "hectare", "sqmeter")
        assert result == pytest.approx(10000.0)

    def test_acre_to_hectare(self) -> None:
        result = convert_area(1.0, "acre", "hectare")
        assert result == pytest.approx(0.40468564224, rel=1e-5)

    def test_sqfoot_to_sqmeter(self) -> None:
        result = convert_area(1.0, "sqfoot", "sqmeter")
        assert result == pytest.approx(0.092903, rel=1e-4)

    def test_sqinch_to_sqcentimeter(self) -> None:
        result = convert_area(1.0, "sqinch", "sqcentimeter")
        assert result == pytest.approx(6.4516, rel=1e-3)

    def test_sqmile_to_acre(self) -> None:
        result = convert_area(1.0, "sqmile", "acre")
        assert result == pytest.approx(640.0, rel=1e-3)

    def test_invalid_unit(self) -> None:
        with pytest.raises(ValueError, match="Unknown area unit"):
            convert_area(1.0, "invalid", "sqmeter")

    def test_all_units_defined(self) -> None:
        expected_ids = {
            "sqmeter",
            "sqkilometer",
            "sqcentimeter",
            "sqmillimeter",
            "sqmicrometer",
            "hectare",
            "sqmile",
            "sqyard",
            "sqfoot",
            "sqinch",
            "acre",
        }
        actual_ids = {u.id for u in AREA_UNITS}
        assert actual_ids == expected_ids

    def test_sqyard_to_sqfoot(self) -> None:
        result = convert_area(1.0, "sqyard", "sqfoot")
        assert result == pytest.approx(9.0, rel=1e-2)


class TestVolumeOperations:
    """Tests for volume conversion operations."""

    def test_liter_to_milliliter(self) -> None:
        result = convert_volume(1.0, "liter", "milliliter")
        assert result == pytest.approx(1000.0)

    def test_cubicmeter_to_liter(self) -> None:
        result = convert_volume(1.0, "cubicmeter", "liter")
        assert result == pytest.approx(1000.0)

    def test_usgallon_to_liter(self) -> None:
        result = convert_volume(1.0, "usgallon", "liter")
        assert result == pytest.approx(3.78541, rel=1e-3)

    def test_usquart_to_uspint(self) -> None:
        result = convert_volume(1.0, "usquart", "uspint")
        assert result == pytest.approx(2.0, rel=1e-2)

    def test_uscup_to_usfluidounce(self) -> None:
        result = convert_volume(1.0, "uscup", "usfluidounce")
        assert result == pytest.approx(8.0, rel=1e-1)

    def test_cubickilometer_to_cubicmeter(self) -> None:
        result = convert_volume(1.0, "cubickilometer", "cubicmeter")
        assert result == pytest.approx(1e9)

    def test_cubiccentimeter_to_milliliter(self) -> None:
        result = convert_volume(1.0, "cubiccentimeter", "milliliter")
        assert result == pytest.approx(1.0)

    def test_invalid_unit(self) -> None:
        with pytest.raises(ValueError, match="Unknown volume unit"):
            convert_volume(1.0, "invalid", "liter")

    def test_all_units_defined(self) -> None:
        expected_ids = {
            "cubicmeter",
            "cubickilometer",
            "cubiccentimeter",
            "cubicmillimeter",
            "liter",
            "milliliter",
            "usgallon",
            "usquart",
            "uspint",
            "uscup",
            "usfluidounce",
        }
        actual_ids = {u.id for u in VOLUME_UNITS}
        assert actual_ids == expected_ids


class TestWeightOperations:
    """Tests for weight conversion operations."""

    def test_kilogram_to_gram(self) -> None:
        result = convert_weight(1.0, "kilogram", "gram")
        assert result == pytest.approx(1000.0)

    def test_kilogram_to_pound(self) -> None:
        result = convert_weight(1.0, "kilogram", "pound")
        assert result == pytest.approx(2.20462, rel=1e-3)

    def test_pound_to_ounce(self) -> None:
        result = convert_weight(1.0, "pound", "ounce")
        assert result == pytest.approx(16.0, rel=1e-2)

    def test_metricton_to_kilogram(self) -> None:
        result = convert_weight(1.0, "metricton", "kilogram")
        assert result == pytest.approx(1000.0)

    def test_gram_to_milligram(self) -> None:
        result = convert_weight(1.0, "gram", "milligram")
        assert result == pytest.approx(1000.0)

    def test_carat_to_gram(self) -> None:
        result = convert_weight(1.0, "carat", "gram")
        assert result == pytest.approx(0.2)

    def test_longton_to_shortton(self) -> None:
        result = convert_weight(1.0, "longton", "shortton")
        assert result == pytest.approx(1.12, rel=1e-2)

    def test_amu_to_kilogram(self) -> None:
        result = convert_weight(1.0, "amu", "kilogram")
        assert result == pytest.approx(1.66053906660e-27, rel=1e-5)

    def test_invalid_unit(self) -> None:
        with pytest.raises(ValueError, match="Unknown weight unit"):
            convert_weight(1.0, "invalid", "kilogram")

    def test_all_units_defined(self) -> None:
        expected_ids = {
            "kilogram",
            "gram",
            "milligram",
            "metricton",
            "longton",
            "shortton",
            "pound",
            "ounce",
            "carat",
            "amu",
        }
        actual_ids = {u.id for u in WEIGHT_UNITS}
        assert actual_ids == expected_ids


class TestTimeOperations:
    """Tests for time conversion operations."""

    def test_minute_to_second(self) -> None:
        result = convert_time(1.0, "minute", "second")
        assert result == pytest.approx(60.0)

    def test_hour_to_minute(self) -> None:
        result = convert_time(1.0, "hour", "minute")
        assert result == pytest.approx(60.0)

    def test_day_to_hour(self) -> None:
        result = convert_time(1.0, "day", "hour")
        assert result == pytest.approx(24.0)

    def test_week_to_day(self) -> None:
        result = convert_time(1.0, "week", "day")
        assert result == pytest.approx(7.0)

    def test_year_to_day(self) -> None:
        result = convert_time(1.0, "year", "day")
        assert result == pytest.approx(365.0)

    def test_second_to_millisecond(self) -> None:
        result = convert_time(1.0, "second", "millisecond")
        assert result == pytest.approx(1000.0)

    def test_millisecond_to_microsecond(self) -> None:
        result = convert_time(1.0, "millisecond", "microsecond")
        assert result == pytest.approx(1000.0)

    def test_microsecond_to_nanosecond(self) -> None:
        result = convert_time(1.0, "microsecond", "nanosecond")
        assert result == pytest.approx(1000.0)

    def test_nanosecond_to_picosecond(self) -> None:
        result = convert_time(1.0, "nanosecond", "picosecond")
        assert result == pytest.approx(1000.0)

    def test_month_to_day(self) -> None:
        result = convert_time(1.0, "month", "day")
        assert result == pytest.approx(30.0)

    def test_invalid_unit(self) -> None:
        with pytest.raises(ValueError, match="Unknown time unit"):
            convert_time(1.0, "invalid", "second")

    def test_all_units_defined(self) -> None:
        expected_ids = {
            "second",
            "millisecond",
            "microsecond",
            "nanosecond",
            "picosecond",
            "minute",
            "hour",
            "day",
            "week",
            "month",
            "year",
        }
        actual_ids = {u.id for u in TIME_UNITS}
        assert actual_ids == expected_ids
