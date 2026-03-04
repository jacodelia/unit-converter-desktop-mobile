"""Unit tests for the internationalization system."""

import pytest

from unitconverter.i18n.translations import (
    TranslationService,
    TRANSLATIONS,
    LANGUAGE_NAMES,
    SUPPORTED_LANGUAGES,
    APP_TITLE,
    FROM_LABEL,
    TO_LABEL,
    CAT_LENGTH,
    CAT_TEMPERATURE,
)


class TestTranslationService:
    """Tests for the TranslationService."""

    def test_default_language_is_english(self) -> None:
        service = TranslationService()
        assert service.language == "en"

    def test_set_language(self) -> None:
        service = TranslationService()
        service.language = "es"
        assert service.language == "es"

    def test_set_invalid_language(self) -> None:
        service = TranslationService()
        service.language = "invalid"
        assert service.language == "en"

    def test_init_with_language(self) -> None:
        service = TranslationService(language="fr")
        assert service.language == "fr"

    def test_init_with_invalid_language(self) -> None:
        service = TranslationService(language="invalid")
        assert service.language == "en"

    def test_get_english(self) -> None:
        service = TranslationService(language="en")
        assert service.get(APP_TITLE) == "Unit Converter"

    def test_get_spanish(self) -> None:
        service = TranslationService(language="es")
        assert service.get(APP_TITLE) == "Conversor de Unidades"

    def test_get_french(self) -> None:
        service = TranslationService(language="fr")
        assert service.get(APP_TITLE) == "Convertisseur d'Unités"

    def test_get_italian(self) -> None:
        service = TranslationService(language="it")
        assert service.get(APP_TITLE) == "Convertitore di Unità"

    def test_get_german(self) -> None:
        service = TranslationService(language="de")
        assert service.get(APP_TITLE) == "Einheitenumrechner"

    def test_get_russian(self) -> None:
        service = TranslationService(language="ru")
        assert service.get(APP_TITLE) == "Конвертер Единиц"

    def test_get_japanese(self) -> None:
        service = TranslationService(language="ja")
        assert service.get(APP_TITLE) == "単位変換"

    def test_get_chinese(self) -> None:
        service = TranslationService(language="zh")
        assert service.get(APP_TITLE) == "单位转换器"

    def test_get_fallback_to_english(self) -> None:
        service = TranslationService(language="es")
        result = service.get("nonexistent_key")
        # Should return the key itself as fallback
        assert result == "nonexistent_key"

    def test_get_language_name(self) -> None:
        assert TranslationService.get_language_name("en") == "English"
        assert TranslationService.get_language_name("es") == "Español"
        assert TranslationService.get_language_name("fr") == "Français"

    def test_get_language_name_unknown(self) -> None:
        assert TranslationService.get_language_name("xx") == "xx"

    def test_all_languages_have_app_title(self) -> None:
        for lang in SUPPORTED_LANGUAGES:
            assert APP_TITLE in TRANSLATIONS[lang]

    def test_all_languages_have_from_label(self) -> None:
        for lang in SUPPORTED_LANGUAGES:
            assert FROM_LABEL in TRANSLATIONS[lang]

    def test_all_languages_have_to_label(self) -> None:
        for lang in SUPPORTED_LANGUAGES:
            assert TO_LABEL in TRANSLATIONS[lang]

    def test_all_languages_have_category_names(self) -> None:
        for lang in SUPPORTED_LANGUAGES:
            assert CAT_LENGTH in TRANSLATIONS[lang]
            assert CAT_TEMPERATURE in TRANSLATIONS[lang]

    def test_supported_languages_count(self) -> None:
        assert len(SUPPORTED_LANGUAGES) == 8

    def test_language_names_count(self) -> None:
        assert len(LANGUAGE_NAMES) == 8

    def test_all_supported_languages_have_names(self) -> None:
        for lang in SUPPORTED_LANGUAGES:
            assert lang in LANGUAGE_NAMES
