"""Entry point for the Unit Converter Mobile application.

Detects the platform at startup:
- Desktop (Linux/macOS/Windows): launches the PySide6 Qt UI.
- Android/iOS: launches the Toga native UI.

Usage (desktop):
    python main.py                 # Auto-detect form factor
    python main.py --phone         # Force phone layout
    python main.py --tablet        # Force tablet layout
"""

import sys

from unitconverter.services.converter_service import ConverterService
from unitconverter.services.search_service import SearchService
from unitconverter.i18n.translations import TranslationService
from unitconverter.viewmodels.converter_viewmodel import ConverterViewModel
from unitconverter.viewmodels.search_viewmodel import SearchViewModel
from unitconverter.viewmodels.preferences_viewmodel import PreferencesViewModel


def _is_mobile_platform() -> bool:
    """Return True if running on Android or iOS."""
    try:
        import android  # noqa: F401 – Chaquopy injects this on Android

        return True
    except ImportError:
        pass
    try:
        import rubicon.objc  # noqa: F401 – available on iOS via Briefcase

        return True
    except ImportError:
        pass
    return False


def _run_desktop() -> int:
    """Launch the PySide6 desktop UI. Returns the exit code."""
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QFont

    from unitconverter.views.mobile_view import MobileWindow

    app = QApplication(sys.argv)
    font = QFont("Inter", 10)
    app.setFont(font)

    # Parse command-line form factor
    form_factor = "auto"
    if "--tablet" in sys.argv:
        form_factor = "tablet"
    elif "--phone" in sys.argv:
        form_factor = "phone"

    device = _make_device_profile(app, form_factor)

    converter_service = ConverterService()
    search_service = SearchService(converter_service)
    translation_service = TranslationService(language="en")

    converter_vm = ConverterViewModel(converter_service)
    search_vm = SearchViewModel(search_service, converter_vm)
    prefs_vm = PreferencesViewModel(translation_service)

    window = MobileWindow(converter_vm, search_vm, prefs_vm, device)
    window.show()

    return app.exec()


def _make_device_profile(app, form_factor: str):
    """Create a DeviceProfile for the desktop window size."""

    class DeviceProfile:
        PHONE_WIDTH = 390
        PHONE_HEIGHT = 844
        TABLET_WIDTH = 1024
        TABLET_HEIGHT = 768

        def __init__(self, ff: str) -> None:
            if ff == "tablet":
                self.form_factor = "tablet"
            elif ff == "phone":
                self.form_factor = "phone"
            else:
                self.form_factor = self._detect(app)

        @staticmethod
        def _detect(application) -> str:
            screen = application.primaryScreen()
            if screen:
                size = screen.availableSize()
                diagonal = (
                    (size.width() ** 2 + size.height() ** 2) ** 0.5
                ) / screen.logicalDotsPerInch()
                if diagonal >= 9.0:
                    return "tablet"
            return "phone"

        @property
        def is_tablet(self) -> bool:
            return self.form_factor == "tablet"

        @property
        def width(self) -> int:
            return self.TABLET_WIDTH if self.is_tablet else self.PHONE_WIDTH

        @property
        def height(self) -> int:
            return self.TABLET_HEIGHT if self.is_tablet else self.PHONE_HEIGHT

    return DeviceProfile(form_factor)


def _run_mobile() -> int:
    """Launch the Toga mobile UI. Returns 0."""
    from unitconverter.views.toga_view import TogaMobileApp

    converter_service = ConverterService()
    search_service = SearchService(converter_service)
    translation_service = TranslationService(language="en")

    converter_vm = ConverterViewModel(converter_service)
    search_vm = SearchViewModel(search_service, converter_vm)
    prefs_vm = PreferencesViewModel(translation_service)

    app = TogaMobileApp(converter_vm, search_vm, prefs_vm)
    app.main_loop()
    return 0


def main() -> int:
    """Application entry point.

    Returns:
        Exit code from the UI event loop.
    """
    if _is_mobile_platform():
        return _run_mobile()
    return _run_desktop()


if __name__ == "__main__":
    sys.exit(main())
