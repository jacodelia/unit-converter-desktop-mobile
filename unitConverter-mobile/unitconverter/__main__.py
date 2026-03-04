"""Briefcase Android/iOS entry point.

When Briefcase launches the app on mobile, it runs::

    runpy.run_module("unitconverter", run_name="__main__")

which executes this file.  It wires up the services, ViewModels,
and the Toga UI — the same work that main.py:_run_mobile() does on
the desktop code-path.
"""

from unitconverter.services.converter_service import ConverterService
from unitconverter.services.search_service import SearchService
from unitconverter.i18n.translations import TranslationService
from unitconverter.viewmodels.converter_viewmodel import ConverterViewModel
from unitconverter.viewmodels.search_viewmodel import SearchViewModel
from unitconverter.viewmodels.preferences_viewmodel import PreferencesViewModel
from unitconverter.views.toga_view import TogaMobileApp


def main():
    converter_service = ConverterService()
    search_service = SearchService(converter_service)
    translation_service = TranslationService(language="en")

    converter_vm = ConverterViewModel(converter_service)
    search_vm = SearchViewModel(search_service, converter_vm)
    prefs_vm = PreferencesViewModel(translation_service)

    return TogaMobileApp(converter_vm, search_vm, prefs_vm)


main().main_loop()
