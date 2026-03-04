"""Internationalization translations for 8 languages.

Supported languages:
    - English (en)
    - Spanish (es)
    - French (fr)
    - Italian (it)
    - German (de)
    - Russian (ru)
    - Japanese (ja)
    - Chinese (zh)
"""

from typing import Optional


# Translation key constants
APP_TITLE = "app_title"
FROM_LABEL = "from_label"
TO_LABEL = "to_label"
SEARCH_PLACEHOLDER = "search_placeholder"
SETTINGS = "settings"
LANGUAGE = "language"
HISTORY = "history"
HOME = "home"
NO_CONVERSIONS = "no_conversions"
RECENT_CONVERSIONS = "recent_conversions"
CLEAR_ALL = "clear_all"
QUICK_REFERENCE = "quick_reference"
CONVERSION_HISTORY = "conversion_history"
ENTER_VALUE = "enter_value"
PREFERENCES = "preferences"
SEARCH_UNITS = "search_units"

# Category names
CAT_LENGTH = "cat_length"
CAT_TEMPERATURE = "cat_temperature"
CAT_AREA = "cat_area"
CAT_VOLUME = "cat_volume"
CAT_WEIGHT = "cat_weight"
CAT_TIME = "cat_time"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        APP_TITLE: "Unit Converter",
        FROM_LABEL: "From",
        TO_LABEL: "To",
        SEARCH_PLACEHOLDER: "Search units...",
        SETTINGS: "Settings",
        LANGUAGE: "Language",
        HISTORY: "History",
        HOME: "Home",
        NO_CONVERSIONS: "No conversions yet",
        RECENT_CONVERSIONS: "Recent Conversions",
        CLEAR_ALL: "Clear All",
        QUICK_REFERENCE: "Quick Reference",
        CONVERSION_HISTORY: "Conversion History",
        ENTER_VALUE: "Enter value",
        PREFERENCES: "Preferences",
        SEARCH_UNITS: "Search units...",
        CAT_LENGTH: "Length",
        CAT_TEMPERATURE: "Temperature",
        CAT_AREA: "Area",
        CAT_VOLUME: "Volume",
        CAT_WEIGHT: "Weight",
        CAT_TIME: "Time",
    },
    "es": {
        APP_TITLE: "Conversor de Unidades",
        FROM_LABEL: "De",
        TO_LABEL: "A",
        SEARCH_PLACEHOLDER: "Buscar unidades...",
        SETTINGS: "Configuración",
        LANGUAGE: "Idioma",
        HISTORY: "Historial",
        HOME: "Inicio",
        NO_CONVERSIONS: "Sin conversiones aún",
        RECENT_CONVERSIONS: "Conversiones Recientes",
        CLEAR_ALL: "Limpiar Todo",
        QUICK_REFERENCE: "Referencia Rápida",
        CONVERSION_HISTORY: "Historial de Conversiones",
        ENTER_VALUE: "Ingrese valor",
        PREFERENCES: "Preferencias",
        SEARCH_UNITS: "Buscar unidades...",
        CAT_LENGTH: "Longitud",
        CAT_TEMPERATURE: "Temperatura",
        CAT_AREA: "Área",
        CAT_VOLUME: "Volumen",
        CAT_WEIGHT: "Peso",
        CAT_TIME: "Tiempo",
    },
    "fr": {
        APP_TITLE: "Convertisseur d'Unités",
        FROM_LABEL: "De",
        TO_LABEL: "À",
        SEARCH_PLACEHOLDER: "Rechercher des unités...",
        SETTINGS: "Paramètres",
        LANGUAGE: "Langue",
        HISTORY: "Historique",
        HOME: "Accueil",
        NO_CONVERSIONS: "Aucune conversion",
        RECENT_CONVERSIONS: "Conversions Récentes",
        CLEAR_ALL: "Tout Effacer",
        QUICK_REFERENCE: "Référence Rapide",
        CONVERSION_HISTORY: "Historique des Conversions",
        ENTER_VALUE: "Entrez la valeur",
        PREFERENCES: "Préférences",
        SEARCH_UNITS: "Rechercher des unités...",
        CAT_LENGTH: "Longueur",
        CAT_TEMPERATURE: "Température",
        CAT_AREA: "Surface",
        CAT_VOLUME: "Volume",
        CAT_WEIGHT: "Poids",
        CAT_TIME: "Temps",
    },
    "it": {
        APP_TITLE: "Convertitore di Unità",
        FROM_LABEL: "Da",
        TO_LABEL: "A",
        SEARCH_PLACEHOLDER: "Cerca unità...",
        SETTINGS: "Impostazioni",
        LANGUAGE: "Lingua",
        HISTORY: "Cronologia",
        HOME: "Home",
        NO_CONVERSIONS: "Nessuna conversione",
        RECENT_CONVERSIONS: "Conversioni Recenti",
        CLEAR_ALL: "Cancella Tutto",
        QUICK_REFERENCE: "Riferimento Rapido",
        CONVERSION_HISTORY: "Cronologia Conversioni",
        ENTER_VALUE: "Inserisci valore",
        PREFERENCES: "Preferenze",
        SEARCH_UNITS: "Cerca unità...",
        CAT_LENGTH: "Lunghezza",
        CAT_TEMPERATURE: "Temperatura",
        CAT_AREA: "Area",
        CAT_VOLUME: "Volume",
        CAT_WEIGHT: "Peso",
        CAT_TIME: "Tempo",
    },
    "de": {
        APP_TITLE: "Einheitenumrechner",
        FROM_LABEL: "Von",
        TO_LABEL: "Nach",
        SEARCH_PLACEHOLDER: "Einheiten suchen...",
        SETTINGS: "Einstellungen",
        LANGUAGE: "Sprache",
        HISTORY: "Verlauf",
        HOME: "Start",
        NO_CONVERSIONS: "Noch keine Umrechnungen",
        RECENT_CONVERSIONS: "Letzte Umrechnungen",
        CLEAR_ALL: "Alles Löschen",
        QUICK_REFERENCE: "Schnellreferenz",
        CONVERSION_HISTORY: "Umrechnungsverlauf",
        ENTER_VALUE: "Wert eingeben",
        PREFERENCES: "Einstellungen",
        SEARCH_UNITS: "Einheiten suchen...",
        CAT_LENGTH: "Länge",
        CAT_TEMPERATURE: "Temperatur",
        CAT_AREA: "Fläche",
        CAT_VOLUME: "Volumen",
        CAT_WEIGHT: "Gewicht",
        CAT_TIME: "Zeit",
    },
    "ru": {
        APP_TITLE: "Конвертер Единиц",
        FROM_LABEL: "Из",
        TO_LABEL: "В",
        SEARCH_PLACEHOLDER: "Поиск единиц...",
        SETTINGS: "Настройки",
        LANGUAGE: "Язык",
        HISTORY: "История",
        HOME: "Главная",
        NO_CONVERSIONS: "Пока нет конверсий",
        RECENT_CONVERSIONS: "Последние Конверсии",
        CLEAR_ALL: "Очистить Все",
        QUICK_REFERENCE: "Быстрая Справка",
        CONVERSION_HISTORY: "История Конверсий",
        ENTER_VALUE: "Введите значение",
        PREFERENCES: "Предпочтения",
        SEARCH_UNITS: "Поиск единиц...",
        CAT_LENGTH: "Длина",
        CAT_TEMPERATURE: "Температура",
        CAT_AREA: "Площадь",
        CAT_VOLUME: "Объём",
        CAT_WEIGHT: "Вес",
        CAT_TIME: "Время",
    },
    "ja": {
        APP_TITLE: "単位変換",
        FROM_LABEL: "変換元",
        TO_LABEL: "変換先",
        SEARCH_PLACEHOLDER: "単位を検索...",
        SETTINGS: "設定",
        LANGUAGE: "言語",
        HISTORY: "履歴",
        HOME: "ホーム",
        NO_CONVERSIONS: "変換履歴なし",
        RECENT_CONVERSIONS: "最近の変換",
        CLEAR_ALL: "すべてクリア",
        QUICK_REFERENCE: "クイックリファレンス",
        CONVERSION_HISTORY: "変換履歴",
        ENTER_VALUE: "値を入力",
        PREFERENCES: "設定",
        SEARCH_UNITS: "単位を検索...",
        CAT_LENGTH: "長さ",
        CAT_TEMPERATURE: "温度",
        CAT_AREA: "面積",
        CAT_VOLUME: "体積",
        CAT_WEIGHT: "重さ",
        CAT_TIME: "時間",
    },
    "zh": {
        APP_TITLE: "单位转换器",
        FROM_LABEL: "从",
        TO_LABEL: "到",
        SEARCH_PLACEHOLDER: "搜索单位...",
        SETTINGS: "设置",
        LANGUAGE: "语言",
        HISTORY: "历史",
        HOME: "首页",
        NO_CONVERSIONS: "暂无转换记录",
        RECENT_CONVERSIONS: "最近的转换",
        CLEAR_ALL: "清除全部",
        QUICK_REFERENCE: "快速参考",
        CONVERSION_HISTORY: "转换历史",
        ENTER_VALUE: "输入数值",
        PREFERENCES: "偏好设置",
        SEARCH_UNITS: "搜索单位...",
        CAT_LENGTH: "长度",
        CAT_TEMPERATURE: "温度",
        CAT_AREA: "面积",
        CAT_VOLUME: "体积",
        CAT_WEIGHT: "重量",
        CAT_TIME: "时间",
    },
}

# Language display names (shown in language selector)
LANGUAGE_NAMES: dict[str, str] = {
    "en": "English",
    "es": "Español",
    "fr": "Français",
    "it": "Italiano",
    "de": "Deutsch",
    "ru": "Русский",
    "ja": "日本語",
    "zh": "中文",
}

SUPPORTED_LANGUAGES: tuple[str, ...] = tuple(TRANSLATIONS.keys())


class TranslationService:
    """Service for retrieving translated strings.

    Provides a simple interface to get translated text based on the
    current language setting, with English as the fallback.
    """

    def __init__(self, language: str = "en") -> None:
        """Initialize with a language code.

        Args:
            language: ISO 639-1 language code (default: 'en').
        """
        self._language = language if language in TRANSLATIONS else "en"

    @property
    def language(self) -> str:
        """Return the current language code."""
        return self._language

    @language.setter
    def language(self, value: str) -> None:
        """Set the current language.

        Args:
            value: ISO 639-1 language code.
        """
        if value in TRANSLATIONS:
            self._language = value

    def get(self, key: str) -> str:
        """Get a translated string for the given key.

        Falls back to English if the key is not found in the
        current language.

        Args:
            key: The translation key.

        Returns:
            The translated string.
        """
        lang_dict = TRANSLATIONS.get(self._language, TRANSLATIONS["en"])
        return lang_dict.get(key, TRANSLATIONS["en"].get(key, key))

    @staticmethod
    def get_language_name(code: str) -> str:
        """Get the display name for a language code.

        Args:
            code: ISO 639-1 language code.

        Returns:
            The display name of the language.
        """
        return LANGUAGE_NAMES.get(code, code)
