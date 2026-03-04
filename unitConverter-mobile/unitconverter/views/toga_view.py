"""Toga-based mobile view for Android and iOS.

Mirrors the desktop mobile_view.py design as closely as Toga allows:
- Header with app icon, title
- Search bar
- Horizontal category pill buttons
- Conversion card panel (From / Swap / To)
- History section
- Bottom navigation bar (Home, History, Settings)
- Language/preferences dialog via Settings

Bottom navigation behaviour:
- Home:     shows the converter (search + pills + card + recent history)
- History:  shows a dedicated full-screen history list with a Clear button
- Settings: opens a language-selection dialog

The glassmorphism dark gradient look from the desktop Qt version is
approximated using Toga's Pack layout and color properties.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, BOLD

from unitconverter.viewmodels.converter_viewmodel import ConverterViewModel
from unitconverter.viewmodels.search_viewmodel import SearchViewModel
from unitconverter.viewmodels.preferences_viewmodel import PreferencesViewModel
from unitconverter.i18n.translations import (
    APP_TITLE,
    FROM_LABEL,
    TO_LABEL,
    SEARCH_PLACEHOLDER,
    ENTER_VALUE,
    NO_CONVERSIONS,
    RECENT_CONVERSIONS,
    CONVERSION_HISTORY,
    CLEAR_ALL,
    HOME,
    HISTORY,
    SETTINGS,
    PREFERENCES,
    LANGUAGE,
    CAT_LENGTH,
    CAT_TEMPERATURE,
    CAT_AREA,
    CAT_VOLUME,
    CAT_WEIGHT,
    CAT_TIME,
)

# ── Colour palette (matching desktop glassmorphism) ──────────────────
BG_DARK = "#0F0C29"
BG_MID = "#302B63"
BG_CARD = "#2A2650"  # lighter card background
ACCENT = "#7F5AF0"
ACCENT2 = "#6C63FF"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#9090B0"
TEXT_DIM = "#606080"

CATEGORY_I18N_KEYS = {
    "length": CAT_LENGTH,
    "temperature": CAT_TEMPERATURE,
    "area": CAT_AREA,
    "volume": CAT_VOLUME,
    "weight": CAT_WEIGHT,
    "time": CAT_TIME,
}

CATEGORY_ICONS = {
    "length": "\U0001f4cf",  # ruler
    "temperature": "\U0001f321",  # thermometer
    "area": "\U00002b1c",  # white square
    "volume": "\U0001f9ca",  # ice cube
    "weight": "\u2696",  # balance scale
    "time": "\u23f0",  # alarm clock
}


class TogaMobileApp(toga.App):
    """Toga application for the Unit Converter on Android/iOS."""

    def __init__(
        self,
        converter_vm: ConverterViewModel,
        search_vm: SearchViewModel,
        prefs_vm: PreferencesViewModel,
    ) -> None:
        self._converter_vm = converter_vm
        self._search_vm = search_vm
        self._prefs_vm = prefs_vm
        self._updating = False  # guard against cascading updates
        self._pill_buttons: dict[str, toga.Button] = {}
        self._current_nav = "home"
        super().__init__(
            formal_name="Unit Converter",
            app_id="com.unitconverter",
            app_name="unitconverter",
        )

    # ================================================================
    # Startup — build the whole UI
    # ================================================================

    def startup(self) -> None:
        """Build the Toga UI."""
        self.main_window = toga.MainWindow(
            title=self._prefs_vm.get_text(APP_TITLE),
        )

        # ── Build the two "pages" ────────────────────────────────────
        self._home_page = self._build_home_page()
        self._history_page = self._build_history_page()

        # ── Page container (swap pages in/out) ───────────────────────
        self._page_container = toga.Box(
            children=[self._home_page],
            style=Pack(direction=COLUMN, flex=1, background_color=BG_DARK),
        )

        page_scroll = toga.ScrollContainer(
            content=self._page_container,
            style=Pack(flex=1, background_color=BG_DARK),
        )

        # ── Bottom navigation ────────────────────────────────────────
        bottom_nav = self._build_bottom_nav()

        # ── Root container ───────────────────────────────────────────
        root = toga.Box(
            children=[page_scroll, bottom_nav],
            style=Pack(direction=COLUMN, background_color=BG_DARK),
        )

        self.main_window.content = root
        self.main_window.show()

        # ── Connect ViewModel events ─────────────────────────────────
        self._converter_vm.on("category_changed", self._vm_category_changed)
        self._converter_vm.on("result_changed", self._vm_result_changed)
        self._converter_vm.on("history_changed", self._vm_history_changed)
        self._prefs_vm.on("language_changed", self._vm_language_changed)

        # initial conversion display
        self._update_result_display()

    # ================================================================
    # Page builders
    # ================================================================

    def _build_home_page(self) -> toga.Box:
        """Build the main Home page (converter + mini history)."""
        header = self._build_header()
        search_box = self._build_search_bar()
        pills_box = self._build_category_pills()
        card_box = self._build_conversion_card()
        history_box = self._build_mini_history()

        return toga.Box(
            children=[
                header,
                search_box,
                pills_box,
                card_box,
                history_box,
                toga.Box(style=Pack(height=80)),  # spacer for bottom nav
            ],
            style=Pack(direction=COLUMN, background_color=BG_DARK),
        )

    def _build_history_page(self) -> toga.Box:
        """Build the dedicated History page."""
        self._history_page_title = toga.Label(
            self._prefs_vm.get_text(CONVERSION_HISTORY),
            style=Pack(
                font_weight=BOLD,
                font_size=18,
                color=TEXT_PRIMARY,
                margin=16,
                text_align=CENTER,
            ),
        )

        self._clear_btn = toga.Button(
            self._prefs_vm.get_text(CLEAR_ALL),
            on_press=self._on_clear_history,
            style=Pack(
                height=44,
                margin_left=16,
                margin_right=16,
                margin_bottom=12,
                color=TEXT_PRIMARY,
                background_color=ACCENT,
            ),
        )

        self._history_page_label = toga.Label(
            self._prefs_vm.get_text(NO_CONVERSIONS),
            style=Pack(
                font_size=14,
                color=TEXT_SECONDARY,
                margin=16,
                text_align=CENTER,
            ),
        )

        return toga.Box(
            children=[
                self._history_page_title,
                self._clear_btn,
                self._history_page_label,
                toga.Box(style=Pack(height=80)),
            ],
            style=Pack(direction=COLUMN, background_color=BG_DARK),
        )

    # ================================================================
    # Widget builders
    # ================================================================

    def _build_header(self) -> toga.Box:
        icon_label = toga.Label(
            "\u26a1",
            style=Pack(
                font_size=18,
                color=TEXT_PRIMARY,
                margin_left=16,
                margin_right=8,
                margin_top=16,
                margin_bottom=8,
            ),
        )
        self._title_label = toga.Label(
            self._prefs_vm.get_text(APP_TITLE),
            style=Pack(
                font_weight=BOLD,
                font_size=18,
                color=TEXT_PRIMARY,
                flex=1,
                margin_top=16,
                margin_bottom=8,
            ),
        )
        return toga.Box(
            children=[icon_label, self._title_label],
            style=Pack(direction=ROW, background_color=BG_DARK),
        )

    def _build_search_bar(self) -> toga.Box:
        self._search_input = toga.TextInput(
            placeholder=self._prefs_vm.get_text(SEARCH_PLACEHOLDER),
            on_confirm=self._on_search_confirm,
            style=Pack(
                flex=1,
                margin=8,
                height=44,
                color=TEXT_PRIMARY,
                background_color=BG_MID,
            ),
        )
        return toga.Box(
            children=[self._search_input],
            style=Pack(direction=ROW, background_color=BG_DARK, margin_bottom=4),
        )

    def _build_category_pills(self) -> toga.Box:
        self._pill_buttons.clear()
        children = []
        for cat in self._converter_vm.categories:
            icon = CATEGORY_ICONS.get(cat.id, "")
            i18n_key = CATEGORY_I18N_KEYS.get(cat.id)
            label = self._prefs_vm.get_text(i18n_key) if i18n_key else cat.name
            btn = toga.Button(
                f"{icon} {label}",
                on_press=self._make_pill_handler(cat.id),
                style=Pack(
                    margin=4,
                    height=40,
                    font_size=13,
                    color=TEXT_PRIMARY,
                    background_color=BG_MID,
                ),
            )
            self._pill_buttons[cat.id] = btn
            children.append(btn)

        self._highlight_active_pill()

        return toga.Box(
            children=children,
            style=Pack(
                direction=ROW,
                margin_left=8,
                margin_right=8,
                margin_bottom=8,
                background_color=BG_DARK,
            ),
        )

    def _build_conversion_card(self) -> toga.Box:
        # ── From ──
        self._from_label = toga.Label(
            self._prefs_vm.get_text(FROM_LABEL),
            style=Pack(
                font_weight=BOLD,
                font_size=13,
                color=ACCENT,
                text_align=CENTER,
                margin_bottom=6,
            ),
        )

        self._from_input = toga.TextInput(
            value="1",
            placeholder=self._prefs_vm.get_text(ENTER_VALUE),
            on_change=self._on_from_value_changed,
            style=Pack(
                flex=1,
                height=48,
                font_size=18,
                text_align=CENTER,
                color=TEXT_PRIMARY,
                background_color=BG_DARK,
                margin_right=8,
            ),
        )

        self._from_unit_select = toga.Selection(
            items=self._get_unit_items(),
            on_change=self._on_from_unit_changed,
            style=Pack(width=110, height=48),
        )
        self._set_selection_value(
            self._from_unit_select, self._converter_vm.from_unit_id
        )

        from_row = toga.Box(
            children=[self._from_input, self._from_unit_select],
            style=Pack(
                direction=ROW,
                margin_bottom=8,
                margin_left=8,
                margin_right=8,
                background_color=BG_CARD,
            ),
        )

        # ── Swap ──
        swap_btn = toga.Button(
            "\u21c5",
            on_press=self._on_swap,
            style=Pack(
                width=52,
                height=52,
                font_size=20,
                color=TEXT_PRIMARY,
                background_color=ACCENT,
            ),
        )
        swap_row = toga.Box(
            children=[swap_btn],
            style=Pack(
                direction=ROW,
                align_items=CENTER,
                justify_content=CENTER,
                margin_top=4,
                margin_bottom=4,
                background_color=BG_CARD,
            ),
        )

        # ── To ──
        self._to_label = toga.Label(
            self._prefs_vm.get_text(TO_LABEL),
            style=Pack(
                font_weight=BOLD,
                font_size=13,
                color=ACCENT,
                text_align=CENTER,
                margin_bottom=6,
            ),
        )

        self._to_input = toga.TextInput(
            readonly=True,
            value=self._converter_vm.to_value,
            style=Pack(
                flex=1,
                height=48,
                font_size=18,
                text_align=CENTER,
                color=TEXT_PRIMARY,
                background_color=BG_DARK,
                margin_right=8,
            ),
        )

        self._to_unit_select = toga.Selection(
            items=self._get_unit_items(),
            on_change=self._on_to_unit_changed,
            style=Pack(width=110, height=48),
        )
        self._set_selection_value(self._to_unit_select, self._converter_vm.to_unit_id)

        to_row = toga.Box(
            children=[self._to_input, self._to_unit_select],
            style=Pack(
                direction=ROW,
                margin_bottom=8,
                margin_left=8,
                margin_right=8,
                background_color=BG_CARD,
            ),
        )

        # ── Card wrapper ──
        card = toga.Box(
            children=[
                self._from_label,
                from_row,
                swap_row,
                self._to_label,
                to_row,
            ],
            style=Pack(
                direction=COLUMN,
                margin=12,
                background_color=BG_CARD,
            ),
        )
        return card

    def _build_mini_history(self) -> toga.Box:
        """Small history preview shown on the Home page."""
        self._history_title = toga.Label(
            self._prefs_vm.get_text(RECENT_CONVERSIONS),
            style=Pack(
                font_weight=BOLD,
                font_size=14,
                color=TEXT_PRIMARY,
                margin_bottom=4,
                text_align=CENTER,
            ),
        )
        self._history_label = toga.Label(
            self._prefs_vm.get_text(NO_CONVERSIONS),
            style=Pack(
                font_size=13,
                color=TEXT_SECONDARY,
                text_align=CENTER,
            ),
        )
        return toga.Box(
            children=[self._history_title, self._history_label],
            style=Pack(
                direction=COLUMN,
                margin=12,
                background_color=BG_CARD,
            ),
        )

    def _build_bottom_nav(self) -> toga.Box:
        self._home_btn = toga.Button(
            f"\U0001f3e0 {self._prefs_vm.get_text(HOME)}",
            on_press=self._on_nav_home,
            style=Pack(
                flex=1,
                height=56,
                font_size=12,
                color=ACCENT,
                background_color=BG_MID,
            ),
        )
        self._history_btn = toga.Button(
            f"\U0001f504 {self._prefs_vm.get_text(HISTORY)}",
            on_press=self._on_nav_history,
            style=Pack(
                flex=1,
                height=56,
                font_size=12,
                color=TEXT_SECONDARY,
                background_color=BG_MID,
            ),
        )
        self._settings_btn = toga.Button(
            f"\u2699 {self._prefs_vm.get_text(SETTINGS)}",
            on_press=self._on_nav_settings,
            style=Pack(
                flex=1,
                height=56,
                font_size=12,
                color=TEXT_SECONDARY,
                background_color=BG_MID,
            ),
        )
        return toga.Box(
            children=[self._home_btn, self._history_btn, self._settings_btn],
            style=Pack(direction=ROW, background_color=BG_MID),
        )

    # ================================================================
    # Helpers
    # ================================================================

    def _get_unit_items(self) -> list[str]:
        return [u.symbol for u in self._converter_vm.current_category.units]

    def _unit_id_for_symbol(self, symbol: str) -> str | None:
        for u in self._converter_vm.current_category.units:
            if u.symbol == symbol:
                return u.id
        return None

    def _set_selection_value(self, selection: toga.Selection, unit_id: str) -> None:
        for u in self._converter_vm.current_category.units:
            if u.id == unit_id:
                try:
                    selection.value = u.symbol
                except (ValueError, AttributeError):
                    pass
                return

    def _refresh_unit_selects(self) -> None:
        """Refresh the from/to Selection items for the current category.

        Uses the ``_updating`` guard to prevent cascading on_change
        callbacks from triggering extra conversions.
        """
        self._updating = True
        try:
            items = self._get_unit_items()
            self._from_unit_select.items = items
            self._to_unit_select.items = items
            self._set_selection_value(
                self._from_unit_select, self._converter_vm.from_unit_id
            )
            self._set_selection_value(
                self._to_unit_select, self._converter_vm.to_unit_id
            )
        finally:
            self._updating = False

    def _update_result_display(self) -> None:
        self._to_input.value = self._converter_vm.to_value

    def _highlight_active_pill(self) -> None:
        active_id = self._converter_vm.current_category_id
        for cat_id, btn in self._pill_buttons.items():
            if cat_id == active_id:
                btn.style.background_color = ACCENT
            else:
                btn.style.background_color = BG_MID

    def _make_pill_handler(self, cat_id: str):
        """Return a closure for a pill button press."""

        def handler(widget: toga.Button) -> None:
            self._converter_vm.set_category(cat_id)

        return handler

    def _show_page(self, page_name: str) -> None:
        """Switch the visible page in the page container."""
        self._current_nav = page_name

        # Update button highlight colours
        self._home_btn.style.color = ACCENT if page_name == "home" else TEXT_SECONDARY
        self._history_btn.style.color = (
            ACCENT if page_name == "history" else TEXT_SECONDARY
        )
        self._settings_btn.style.color = (
            ACCENT if page_name == "settings" else TEXT_SECONDARY
        )

        # Swap content
        self._page_container.clear()
        if page_name == "history":
            self._refresh_history_page()
            self._page_container.add(self._history_page)
        else:
            self._page_container.add(self._home_page)

    def _refresh_history_page(self) -> None:
        """Update the full history page label."""
        history = self._converter_vm.history
        if not history:
            self._history_page_label.text = self._prefs_vm.get_text(NO_CONVERSIONS)
        else:
            lines = []
            for entry in history:
                lines.append(f"{entry.display_string}  ({entry.time_string})")
            self._history_page_label.text = "\n".join(lines)

    # ================================================================
    # Bottom nav handlers
    # ================================================================

    def _on_nav_home(self, widget: toga.Button) -> None:
        """Switch to the Home (converter) page."""
        self._show_page("home")

    def _on_nav_history(self, widget: toga.Button) -> None:
        """Switch to the dedicated History page."""
        self._show_page("history")

    def _on_nav_settings(self, widget: toga.Button) -> None:
        """Open the language-selection preferences dialog."""
        # Highlight the settings button while the dialog is open
        self._settings_btn.style.color = ACCENT

        lang_names = [name for _, name in self._prefs_vm.available_languages]
        lang_codes = [code for code, _ in self._prefs_vm.available_languages]

        # Find current index
        current_code = self._prefs_vm.current_language
        current_idx = 0
        for i, code in enumerate(lang_codes):
            if code == current_code:
                current_idx = i
                break

        # Build dialog content
        title_label = toga.Label(
            self._prefs_vm.get_text(PREFERENCES),
            style=Pack(
                font_weight=BOLD,
                font_size=16,
                color=TEXT_PRIMARY,
                margin_bottom=12,
                text_align=CENTER,
            ),
        )
        lang_label = toga.Label(
            self._prefs_vm.get_text(LANGUAGE),
            style=Pack(
                font_size=14,
                color=TEXT_PRIMARY,
                margin_bottom=8,
                text_align=CENTER,
            ),
        )
        lang_select = toga.Selection(
            items=lang_names,
            style=Pack(flex=1, margin_bottom=16),
        )
        if current_idx < len(lang_names):
            lang_select.value = lang_names[current_idx]

        ok_btn = toga.Button(
            "OK",
            style=Pack(
                height=44,
                color=TEXT_PRIMARY,
                background_color=ACCENT,
            ),
        )

        dialog_box = toga.Box(
            children=[title_label, lang_label, lang_select, ok_btn],
            style=Pack(
                direction=COLUMN,
                margin=24,
                background_color=BG_CARD,
            ),
        )

        prefs_window = toga.Window(
            title=self._prefs_vm.get_text(SETTINGS),
            size=(340, 280),
        )
        prefs_window.content = dialog_box

        def _on_ok(w: toga.Button) -> None:
            selected_name = lang_select.value
            for code, name in self._prefs_vm.available_languages:
                if name == selected_name:
                    self._prefs_vm.set_language(code)
                    break
            prefs_window.close()
            # restore nav highlight to whichever page was active
            self._settings_btn.style.color = (
                ACCENT if self._current_nav == "settings" else TEXT_SECONDARY
            )

        ok_btn.on_press = _on_ok
        prefs_window.show()

    # ================================================================
    # UI event handlers
    # ================================================================

    def _on_from_value_changed(self, widget: toga.TextInput) -> None:
        if self._updating:
            return
        self._converter_vm.set_from_value(widget.value)

    def _on_from_unit_changed(self, widget: toga.Selection) -> None:
        if self._updating:
            return
        uid = self._unit_id_for_symbol(widget.value)
        if uid:
            self._converter_vm.set_from_unit(uid)

    def _on_to_unit_changed(self, widget: toga.Selection) -> None:
        if self._updating:
            return
        uid = self._unit_id_for_symbol(widget.value)
        if uid:
            self._converter_vm.set_to_unit(uid)

    def _on_swap(self, widget: toga.Button) -> None:
        self._converter_vm.swap_units()
        self._refresh_unit_selects()
        self._from_input.value = self._converter_vm.from_value

    def _on_search_confirm(self, widget: toga.TextInput) -> None:
        self._search_vm.search(widget.value)
        self._search_vm.apply_result()
        self._refresh_unit_selects()
        self._from_input.value = self._converter_vm.from_value

    def _on_clear_history(self, widget: toga.Button) -> None:
        """Clear all conversion history."""
        self._converter_vm.clear_history()
        self._refresh_history_page()

    # ================================================================
    # ViewModel event handlers
    # ================================================================

    def _vm_category_changed(self, category_id: str) -> None:
        self._highlight_active_pill()
        self._refresh_unit_selects()

    def _vm_result_changed(self, result: str) -> None:
        self._to_input.value = result

    def _vm_history_changed(self) -> None:
        # Update the mini-history on the Home page
        history = self._converter_vm.history
        if not history:
            self._history_label.text = self._prefs_vm.get_text(NO_CONVERSIONS)
        else:
            lines = [entry.display_string for entry in history[:5]]
            self._history_label.text = "\n".join(lines)

        # If the user is on the History page, refresh that too
        if self._current_nav == "history":
            self._refresh_history_page()

    def _vm_language_changed(self, lang: str) -> None:
        """Refresh all translatable text when the language changes."""
        self._title_label.text = self._prefs_vm.get_text(APP_TITLE)
        self._from_label.text = self._prefs_vm.get_text(FROM_LABEL)
        self._to_label.text = self._prefs_vm.get_text(TO_LABEL)
        self._search_input.placeholder = self._prefs_vm.get_text(SEARCH_PLACEHOLDER)
        self._history_title.text = self._prefs_vm.get_text(RECENT_CONVERSIONS)
        self._history_page_title.text = self._prefs_vm.get_text(CONVERSION_HISTORY)
        self._clear_btn.text = self._prefs_vm.get_text(CLEAR_ALL)
        self._home_btn.text = f"\U0001f3e0 {self._prefs_vm.get_text(HOME)}"
        self._history_btn.text = f"\U0001f504 {self._prefs_vm.get_text(HISTORY)}"
        self._settings_btn.text = f"\u2699 {self._prefs_vm.get_text(SETTINGS)}"
        self.main_window.title = self._prefs_vm.get_text(APP_TITLE)

        # Refresh pill labels
        for cat_id, btn in self._pill_buttons.items():
            icon = CATEGORY_ICONS.get(cat_id, "")
            i18n_key = CATEGORY_I18N_KEYS.get(cat_id)
            label = self._prefs_vm.get_text(i18n_key) if i18n_key else cat_id
            btn.text = f"{icon} {label}"
