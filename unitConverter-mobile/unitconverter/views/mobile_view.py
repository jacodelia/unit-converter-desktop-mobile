"""Mobile main window view matching the reference HTML mobile design.

Implements a glassmorphism dark gradient layout with:
- Horizontal scrollable category pills
- Glass-card conversion panel
- Bottom navigation bar
- Compact mobile-friendly layout (390x844 reference)
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QScrollArea,
    QFrame,
    QSizePolicy,
    QDialog,
)

from unitconverter.viewmodels.converter_viewmodel import ConverterViewModel
from unitconverter.viewmodels.search_viewmodel import SearchViewModel
from unitconverter.viewmodels.preferences_viewmodel import PreferencesViewModel
from unitconverter.i18n.translations import (
    APP_TITLE,
    FROM_LABEL,
    TO_LABEL,
    SEARCH_PLACEHOLDER,
    NO_CONVERSIONS,
    RECENT_CONVERSIONS,
    HOME,
    HISTORY,
    SETTINGS,
    PREFERENCES,
    LANGUAGE,
    ENTER_VALUE,
    CAT_LENGTH,
    CAT_TEMPERATURE,
    CAT_AREA,
    CAT_VOLUME,
    CAT_WEIGHT,
    CAT_TIME,
)
from unitconverter.views.styles import (
    MOBILE_WINDOW_STYLE,
    GLASS_CARD_STYLE,
    GLASS_INPUT_STYLE,
    GLASS_COMBO_STYLE,
    PILL_BUTTON_STYLE,
    PILL_BUTTON_ACTIVE_STYLE,
    SWAP_BUTTON_MOBILE_STYLE,
    BOTTOM_NAV_STYLE,
    NAV_BUTTON_STYLE,
    NAV_BUTTON_ACTIVE_STYLE,
    SEARCH_INPUT_MOBILE_STYLE,
    HISTORY_CARD_STYLE,
    PREFERENCES_DIALOG_MOBILE_STYLE,
    SCROLLBAR_MOBILE_STYLE,
    ACCENT_VIOLET,
    ACCENT_BLUE,
    TEXT_WHITE,
)

CATEGORY_I18N_KEYS = {
    "length": CAT_LENGTH,
    "temperature": CAT_TEMPERATURE,
    "area": CAT_AREA,
    "volume": CAT_VOLUME,
    "weight": CAT_WEIGHT,
    "time": CAT_TIME,
}


class MobilePreferencesDialog(QDialog):
    """Mobile preferences dialog for language selection."""

    def __init__(self, prefs_vm: PreferencesViewModel, parent: QWidget = None) -> None:
        super().__init__(parent)
        self._prefs_vm = prefs_vm
        self.setWindowTitle(prefs_vm.get_text(PREFERENCES))
        self.setFixedSize(340, 220)
        self.setStyleSheet(PREFERENCES_DIALOG_MOBILE_STYLE)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel(self._prefs_vm.get_text(PREFERENCES))
        title.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        lang_label = QLabel(self._prefs_vm.get_text(LANGUAGE))
        layout.addWidget(lang_label)

        self._lang_combo = QComboBox()
        for code, name in self._prefs_vm.available_languages:
            self._lang_combo.addItem(name, code)

        current_idx = next(
            (
                i
                for i, (code, _) in enumerate(self._prefs_vm.available_languages)
                if code == self._prefs_vm.current_language
            ),
            0,
        )
        self._lang_combo.setCurrentIndex(current_idx)
        self._lang_combo.currentIndexChanged.connect(self._on_language_changed)
        layout.addWidget(self._lang_combo)

        layout.addStretch()

        close_btn = QPushButton("OK")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)

    def _on_language_changed(self, index: int) -> None:
        code = self._lang_combo.itemData(index)
        if code:
            self._prefs_vm.set_language(code)


class MobileWindow(QMainWindow):
    """Mobile application window with glassmorphism design.

    Optimized for a phone-like viewport (390x844) with touch-friendly
    controls and a bottom navigation bar.
    """

    def __init__(
        self,
        converter_vm: ConverterViewModel,
        search_vm: SearchViewModel,
        prefs_vm: PreferencesViewModel,
        device=None,
    ) -> None:
        super().__init__()
        self._converter_vm = converter_vm
        self._search_vm = search_vm
        self._prefs_vm = prefs_vm
        self._device = device
        self._pill_buttons: dict[str, QPushButton] = {}
        self._current_nav = "home"
        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.setInterval(300)
        self._search_timer.timeout.connect(self._execute_search)

        width = device.width if device else 390
        height = device.height if device else 844
        self.setWindowTitle("Unit Converter")
        self.setFixedSize(width, height)
        self.setStyleSheet(MOBILE_WINDOW_STYLE)

        self._setup_ui()
        self._connect_signals()
        self._update_pill_active()
        self._update_combos()

    def _setup_ui(self) -> None:
        """Build the complete mobile UI layout."""
        central = QWidget()
        self.setCentralWidget(central)
        outer_layout = QVBoxLayout(central)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet(
            f"QScrollArea {{ background: transparent; border: none; }} "
            f"{SCROLLBAR_MOBILE_STYLE}"
        )

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        content_layout.addWidget(self._create_header())
        content_layout.addWidget(self._create_search_bar())
        content_layout.addWidget(self._create_category_pills())
        content_layout.addWidget(self._create_conversion_card())
        content_layout.addWidget(self._create_history_section())
        content_layout.addStretch()
        # Padding for bottom nav
        spacer = QWidget()
        spacer.setFixedHeight(80)
        content_layout.addWidget(spacer)

        scroll.setWidget(content)
        outer_layout.addWidget(scroll, 1)

        # Bottom navigation
        outer_layout.addWidget(self._create_bottom_nav())

    def _create_header(self) -> QWidget:
        """Create the mobile header with title and menu."""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 24, 24, 16)
        layout.setSpacing(12)

        # App icon
        icon_label = QLabel("⚡")
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(
            f"background-color: rgba(255,255,255,8%); "
            f"border: 1px solid rgba(255,255,255,15%); "
            f"border-radius: 12px; font-size: 20px;"
        )
        layout.addWidget(icon_label)

        self._title_label = QLabel(self._prefs_vm.get_text(APP_TITLE))
        self._title_label.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        self._title_label.setStyleSheet(f"color: {TEXT_WHITE};")
        layout.addWidget(self._title_label)

        layout.addStretch()

        # Menu button
        menu_btn = QPushButton("☰")
        menu_btn.setFixedSize(40, 40)
        menu_btn.setStyleSheet(
            f"QPushButton {{ background-color: rgba(255,255,255,8%); "
            f"border: 1px solid rgba(255,255,255,15%); "
            f"border-radius: 12px; color: {TEXT_WHITE}; font-size: 18px; }}"
        )
        menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(menu_btn)

        return header

    def _create_search_bar(self) -> QWidget:
        """Create the search bar for natural language queries."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 0, 16, 12)

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText(
            self._prefs_vm.get_text(SEARCH_PLACEHOLDER)
        )
        self._search_input.setStyleSheet(SEARCH_INPUT_MOBILE_STYLE)
        self._search_input.setFixedHeight(44)
        self._search_input.textChanged.connect(self._on_search_text_changed)
        self._search_input.returnPressed.connect(self._on_search_enter)
        layout.addWidget(self._search_input)

        return container

    def _create_category_pills(self) -> QWidget:
        """Create the horizontal scrollable category pills."""
        container = QWidget()
        outer_layout = QHBoxLayout(container)
        outer_layout.setContentsMargins(16, 0, 16, 16)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFixedHeight(50)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        pills_widget = QWidget()
        pills_layout = QHBoxLayout(pills_widget)
        pills_layout.setContentsMargins(0, 0, 0, 0)
        pills_layout.setSpacing(8)

        for category in self._converter_vm.categories:
            btn = QPushButton(f"{category.icon} {category.name}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(PILL_BUTTON_STYLE)
            btn.setFixedHeight(40)
            cat_id = category.id
            btn.clicked.connect(
                lambda checked, cid=cat_id: self._on_category_clicked(cid)
            )
            self._pill_buttons[category.id] = btn
            pills_layout.addWidget(btn)

        pills_layout.addStretch()
        scroll.setWidget(pills_widget)
        outer_layout.addWidget(scroll)

        return container

    def _create_conversion_card(self) -> QWidget:
        """Create the glassmorphism conversion card."""
        outer = QWidget()
        outer_layout = QHBoxLayout(outer)
        outer_layout.setContentsMargins(16, 0, 16, 16)

        card = QWidget()
        card.setObjectName("glassCard")
        card.setStyleSheet(GLASS_CARD_STYLE)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # FROM section
        self._from_label = QLabel(self._prefs_vm.get_text(FROM_LABEL))
        self._from_label.setStyleSheet(
            f"color: {ACCENT_VIOLET}; font-size: 13px; font-weight: 500;"
        )
        layout.addWidget(self._from_label)

        from_row = QHBoxLayout()
        from_row.setSpacing(12)

        self._from_input = QLineEdit("1")
        self._from_input.setStyleSheet(GLASS_INPUT_STYLE)
        self._from_input.setPlaceholderText(self._prefs_vm.get_text(ENTER_VALUE))
        self._from_input.textChanged.connect(self._on_from_value_changed)
        from_row.addWidget(self._from_input, 1)

        self._from_combo = QComboBox()
        self._from_combo.setStyleSheet(GLASS_COMBO_STYLE)
        self._from_combo.setMinimumWidth(96)
        self._from_combo.currentIndexChanged.connect(self._on_from_unit_changed)
        from_row.addWidget(self._from_combo)

        layout.addLayout(from_row)

        # SWAP button
        swap_row = QHBoxLayout()
        swap_row.addStretch()
        self._swap_btn = QPushButton("⇅")
        self._swap_btn.setStyleSheet(SWAP_BUTTON_MOBILE_STYLE)
        self._swap_btn.setFont(QFont("Inter", 16))
        self._swap_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._swap_btn.clicked.connect(self._on_swap_clicked)
        swap_row.addWidget(self._swap_btn)
        swap_row.addStretch()
        layout.addLayout(swap_row)

        # TO section
        self._to_label = QLabel(self._prefs_vm.get_text(TO_LABEL))
        self._to_label.setStyleSheet(
            f"color: {ACCENT_VIOLET}; font-size: 13px; font-weight: 500;"
        )
        layout.addWidget(self._to_label)

        to_row = QHBoxLayout()
        to_row.setSpacing(12)

        self._to_input = QLineEdit()
        self._to_input.setStyleSheet(GLASS_INPUT_STYLE)
        self._to_input.setReadOnly(True)
        to_row.addWidget(self._to_input, 1)

        self._to_combo = QComboBox()
        self._to_combo.setStyleSheet(GLASS_COMBO_STYLE)
        self._to_combo.setMinimumWidth(96)
        self._to_combo.currentIndexChanged.connect(self._on_to_unit_changed)
        to_row.addWidget(self._to_combo)

        layout.addLayout(to_row)

        outer_layout.addWidget(card)
        return outer

    def _create_history_section(self) -> QWidget:
        """Create the recent conversions section."""
        outer = QWidget()
        outer_layout = QHBoxLayout(outer)
        outer_layout.setContentsMargins(16, 0, 16, 16)

        card = QWidget()
        card.setObjectName("historyCard")
        card.setStyleSheet(HISTORY_CARD_STYLE)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        self._history_title = QLabel(self._prefs_vm.get_text(RECENT_CONVERSIONS))
        self._history_title.setFont(QFont("Inter", 13, QFont.Weight.DemiBold))
        self._history_title.setStyleSheet(f"color: {TEXT_WHITE};")
        layout.addWidget(self._history_title)

        self._history_container = QVBoxLayout()
        self._history_container.setSpacing(4)
        layout.addLayout(self._history_container)

        self._no_history_label = QLabel(self._prefs_vm.get_text(NO_CONVERSIONS))
        self._no_history_label.setStyleSheet(
            f"color: rgba(255,255,255,0.5); font-size: 13px;"
        )
        self._history_container.addWidget(self._no_history_label)

        outer_layout.addWidget(card)
        return outer

    def _create_bottom_nav(self) -> QWidget:
        """Create the bottom navigation bar."""
        nav = QWidget()
        nav.setObjectName("bottomNav")
        nav.setFixedHeight(72)
        nav.setStyleSheet(BOTTOM_NAV_STYLE)

        layout = QHBoxLayout(nav)
        layout.setContentsMargins(24, 8, 24, 8)
        layout.setSpacing(0)

        # Home
        self._home_btn = QPushButton(f"🏠\n{self._prefs_vm.get_text(HOME)}")
        self._home_btn.setStyleSheet(NAV_BUTTON_ACTIVE_STYLE)
        self._home_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._home_btn.clicked.connect(lambda: self._set_nav("home"))
        layout.addWidget(self._home_btn, 1)

        # History
        self._history_btn = QPushButton(f"🔄\n{self._prefs_vm.get_text(HISTORY)}")
        self._history_btn.setStyleSheet(NAV_BUTTON_STYLE)
        self._history_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._history_btn.clicked.connect(lambda: self._set_nav("history"))
        layout.addWidget(self._history_btn, 1)

        # Settings
        self._settings_btn = QPushButton(f"⚙\n{self._prefs_vm.get_text(SETTINGS)}")
        self._settings_btn.setStyleSheet(NAV_BUTTON_STYLE)
        self._settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._settings_btn.clicked.connect(self._open_preferences)
        layout.addWidget(self._settings_btn, 1)

        return nav

    def _connect_signals(self) -> None:
        """Connect ViewModel events to View updates."""
        self._converter_vm.on("category_changed", self._on_vm_category_changed)
        self._converter_vm.on("result_changed", self._on_vm_result_changed)
        self._converter_vm.on("history_changed", self._on_vm_history_changed)
        self._prefs_vm.on("language_changed", self._on_language_changed)

    # --- Signal handlers ---

    def _on_category_clicked(self, category_id: str) -> None:
        self._converter_vm.set_category(category_id)

    def _on_from_unit_changed(self, index: int) -> None:
        if index < 0:
            return
        unit_id = self._from_combo.itemData(index)
        if unit_id:
            self._converter_vm.set_from_unit(unit_id)

    def _on_to_unit_changed(self, index: int) -> None:
        if index < 0:
            return
        unit_id = self._to_combo.itemData(index)
        if unit_id:
            self._converter_vm.set_to_unit(unit_id)

    def _on_from_value_changed(self, text: str) -> None:
        self._converter_vm.set_from_value(text)

    def _on_swap_clicked(self) -> None:
        self._converter_vm.swap_units()
        self._update_combos()
        self._from_input.setText(self._converter_vm.from_value)

    def _on_search_text_changed(self, text: str) -> None:
        self._search_timer.start()

    def _on_search_enter(self) -> None:
        self._search_timer.stop()
        self._execute_search()
        self._search_vm.apply_result()

    def _execute_search(self) -> None:
        query = self._search_input.text()
        self._search_vm.search(query)

    def _on_vm_category_changed(self, category_id: str) -> None:
        self._update_pill_active()
        self._update_combos()

    def _on_vm_result_changed(self, result: str) -> None:
        self._to_input.setText(result)

    def _on_vm_history_changed(self) -> None:
        self._update_history()

    def _on_language_changed(self, lang: str) -> None:
        self._update_all_texts()

    def _set_nav(self, nav: str) -> None:
        self._current_nav = nav
        self._home_btn.setStyleSheet(
            NAV_BUTTON_ACTIVE_STYLE if nav == "home" else NAV_BUTTON_STYLE
        )
        self._history_btn.setStyleSheet(
            NAV_BUTTON_ACTIVE_STYLE if nav == "history" else NAV_BUTTON_STYLE
        )

    # --- UI update methods ---

    def _update_pill_active(self) -> None:
        """Highlight the active category pill."""
        for cat_id, btn in self._pill_buttons.items():
            if cat_id == self._converter_vm.current_category_id:
                btn.setStyleSheet(PILL_BUTTON_ACTIVE_STYLE)
            else:
                btn.setStyleSheet(PILL_BUTTON_STYLE)

    def _update_combos(self) -> None:
        """Refresh the from/to combo boxes."""
        category = self._converter_vm.current_category

        self._from_combo.blockSignals(True)
        self._to_combo.blockSignals(True)

        self._from_combo.clear()
        self._to_combo.clear()

        for unit in category.units:
            self._from_combo.addItem(unit.symbol, unit.id)
            self._to_combo.addItem(unit.symbol, unit.id)

        from_idx = self._from_combo.findData(self._converter_vm.from_unit_id)
        to_idx = self._to_combo.findData(self._converter_vm.to_unit_id)
        self._from_combo.setCurrentIndex(max(from_idx, 0))
        self._to_combo.setCurrentIndex(max(to_idx, 0))

        self._from_combo.blockSignals(False)
        self._to_combo.blockSignals(False)

    def _update_history(self) -> None:
        """Refresh the history list."""
        while self._history_container.count():
            item = self._history_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        history = self._converter_vm.history
        if not history:
            self._no_history_label = QLabel(self._prefs_vm.get_text(NO_CONVERSIONS))
            self._no_history_label.setStyleSheet(
                f"color: rgba(255,255,255,0.5); font-size: 13px;"
            )
            self._history_container.addWidget(self._no_history_label)
            return

        for entry in history[:5]:
            item = QWidget()
            item_layout = QHBoxLayout(item)
            item_layout.setContentsMargins(0, 8, 0, 8)

            text_label = QLabel(entry.display_string)
            text_label.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 13px;")
            item_layout.addWidget(text_label)

            item_layout.addStretch()

            time_label = QLabel(entry.time_string)
            time_label.setStyleSheet(f"color: rgba(255,255,255,0.5); font-size: 11px;")
            item_layout.addWidget(time_label)

            separator = QFrame()
            separator.setFrameShape(QFrame.Shape.HLine)
            separator.setStyleSheet("color: rgba(255,255,255,0.1); max-height: 1px;")

            self._history_container.addWidget(item)
            self._history_container.addWidget(separator)

    def _update_all_texts(self) -> None:
        """Refresh all translatable text elements."""
        self._title_label.setText(self._prefs_vm.get_text(APP_TITLE))
        self._from_label.setText(self._prefs_vm.get_text(FROM_LABEL))
        self._to_label.setText(self._prefs_vm.get_text(TO_LABEL))
        self._search_input.setPlaceholderText(
            self._prefs_vm.get_text(SEARCH_PLACEHOLDER)
        )
        self._history_title.setText(self._prefs_vm.get_text(RECENT_CONVERSIONS))
        self._home_btn.setText(f"🏠\n{self._prefs_vm.get_text(HOME)}")
        self._history_btn.setText(f"🔄\n{self._prefs_vm.get_text(HISTORY)}")
        self._settings_btn.setText(f"⚙\n{self._prefs_vm.get_text(SETTINGS)}")
        self.setWindowTitle(self._prefs_vm.get_text(APP_TITLE))

    def _open_preferences(self) -> None:
        """Open the mobile preferences dialog."""
        dialog = MobilePreferencesDialog(self._prefs_vm, self)
        dialog.exec()
