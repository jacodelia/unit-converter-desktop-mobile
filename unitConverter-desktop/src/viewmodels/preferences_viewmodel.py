"""ViewModel for application preferences (language selection)."""

from PySide6.QtCore import QObject, Signal, Slot

from src.i18n.translations import (
    LANGUAGE_NAMES,
    SUPPORTED_LANGUAGES,
    TranslationService,
)


class PreferencesViewModel(QObject):
    """ViewModel managing application preferences.

    Signals:
        language_changed: Emitted when the display language changes.
    """

    language_changed = Signal(str)

    def __init__(self, translation_service: TranslationService) -> None:
        """Initialize with a translation service.

        Args:
            translation_service: The service for i18n strings.
        """
        super().__init__()
        self._translation = translation_service

    @property
    def current_language(self) -> str:
        """Return the current language code."""
        return self._translation.language

    @property
    def available_languages(self) -> list[tuple[str, str]]:
        """Return list of (code, display_name) tuples for all languages."""
        return [(code, LANGUAGE_NAMES[code]) for code in SUPPORTED_LANGUAGES]

    @property
    def translation(self) -> TranslationService:
        """Return the translation service."""
        return self._translation

    @Slot(str)
    def set_language(self, language_code: str) -> None:
        """Change the display language.

        Args:
            language_code: ISO 639-1 language code.
        """
        if language_code in SUPPORTED_LANGUAGES:
            self._translation.language = language_code
            self.language_changed.emit(language_code)

    def get_text(self, key: str) -> str:
        """Get a translated string.

        Args:
            key: The translation key.

        Returns:
            The translated string.
        """
        return self._translation.get(key)
