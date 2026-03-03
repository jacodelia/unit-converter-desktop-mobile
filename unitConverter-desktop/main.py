"""Entry point for the Unit Converter Desktop application.

Initializes all services, ViewModels, and launches the desktop window.
"""

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from src.services.converter_service import ConverterService
from src.services.search_service import SearchService
from src.i18n.translations import TranslationService
from src.viewmodels.converter_viewmodel import ConverterViewModel
from src.viewmodels.search_viewmodel import SearchViewModel
from src.viewmodels.preferences_viewmodel import PreferencesViewModel
from src.views.desktop_view import DesktopWindow


def main() -> int:
    """Application entry point.

    Returns:
        Exit code from the Qt event loop.
    """
    app = QApplication(sys.argv)

    # Set default font
    font = QFont("Poppins", 10)
    app.setFont(font)

    # Initialize services
    converter_service = ConverterService()
    search_service = SearchService(converter_service)
    translation_service = TranslationService(language="en")

    # Initialize ViewModels
    converter_vm = ConverterViewModel(converter_service)
    search_vm = SearchViewModel(search_service, converter_vm)
    prefs_vm = PreferencesViewModel(translation_service)

    # Create and show the desktop window
    window = DesktopWindow(converter_vm, search_vm, prefs_vm)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
