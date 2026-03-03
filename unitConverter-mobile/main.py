"""Entry point for the Unit Converter Mobile application.

Initializes all services, ViewModels, and launches the mobile window.
Supports phone (390x844) and tablet (1024x768) form factors.

Usage:
    python main.py                 # Auto-detect form factor
    python main.py --phone         # Force phone layout
    python main.py --tablet        # Force tablet layout
"""

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QScreen

from src.services.converter_service import ConverterService
from src.services.search_service import SearchService
from src.i18n.translations import TranslationService
from src.viewmodels.converter_viewmodel import ConverterViewModel
from src.viewmodels.search_viewmodel import SearchViewModel
from src.viewmodels.preferences_viewmodel import PreferencesViewModel
from src.views.mobile_view import MobileWindow


class DeviceProfile:
    """Encapsulates device form factor detection and dimensions.

    Attributes:
        form_factor: 'phone' or 'tablet'.
        width: Window width in pixels.
        height: Window height in pixels.
        is_tablet: True if running in tablet mode.
    """

    PHONE_WIDTH = 390
    PHONE_HEIGHT = 844
    TABLET_WIDTH = 1024
    TABLET_HEIGHT = 768

    def __init__(self, form_factor: str = "auto") -> None:
        """Initialize with a form factor hint.

        Args:
            form_factor: 'phone', 'tablet', or 'auto' (detect from screen).
        """
        if form_factor == "tablet":
            self.form_factor = "tablet"
        elif form_factor == "phone":
            self.form_factor = "phone"
        else:
            self.form_factor = self._detect()

    @staticmethod
    def _detect() -> str:
        """Detect the form factor from the primary screen size.

        Returns:
            'tablet' if the screen is large enough, otherwise 'phone'.
        """
        screen = QApplication.primaryScreen()
        if screen:
            size = screen.availableSize()
            diagonal_inches = (
                (size.width() ** 2 + size.height() ** 2) ** 0.5
            ) / screen.logicalDotsPerInch()
            if diagonal_inches >= 9.0:
                return "tablet"
        return "phone"

    @property
    def is_tablet(self) -> bool:
        """True if the device profile is tablet."""
        return self.form_factor == "tablet"

    @property
    def width(self) -> int:
        """Return the target window width."""
        return self.TABLET_WIDTH if self.is_tablet else self.PHONE_WIDTH

    @property
    def height(self) -> int:
        """Return the target window height."""
        return self.TABLET_HEIGHT if self.is_tablet else self.PHONE_HEIGHT


def main() -> int:
    """Application entry point.

    Returns:
        Exit code from the Qt event loop.
    """
    app = QApplication(sys.argv)

    # Set default font
    font = QFont("Inter", 10)
    app.setFont(font)

    # Parse command-line form factor
    form_factor = "auto"
    if "--tablet" in sys.argv:
        form_factor = "tablet"
    elif "--phone" in sys.argv:
        form_factor = "phone"

    device = DeviceProfile(form_factor)

    # Initialize services
    converter_service = ConverterService()
    search_service = SearchService(converter_service)
    translation_service = TranslationService(language="en")

    # Initialize ViewModels
    converter_vm = ConverterViewModel(converter_service)
    search_vm = SearchViewModel(search_service, converter_vm)
    prefs_vm = PreferencesViewModel(translation_service)

    # Create and show the mobile window
    window = MobileWindow(converter_vm, search_vm, prefs_vm, device)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
