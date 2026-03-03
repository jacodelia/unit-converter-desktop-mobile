"""Desktop main window view matching the reference HTML design.

Implements a neumorphic dark-mode desktop layout with:
- Left sidebar with category navigation
- Main conversion panel with from/to inputs
- Search bar in the header
- Quick reference table
- Conversion history panel
"""

from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QFont, QIcon, QPainter, QColor, QPen
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QScrollArea,
    QFrame,
    QSizePolicy,
    QSpacerItem,
    QDialog,
)

from src.viewmodels.converter_viewmodel import ConverterViewModel
from src.viewmodels.search_viewmodel import SearchViewModel
from src.viewmodels.preferences_viewmodel import PreferencesViewModel
from src.i18n.translations import (
    APP_TITLE,
    FROM_LABEL,
    TO_LABEL,
    SEARCH_PLACEHOLDER,
    QUICK_REFERENCE,
    CONVERSION_HISTORY,
    NO_CONVERSIONS,
    CLEAR_ALL,
    PREFERENCES,
    LANGUAGE,
    CAT_LENGTH,
    CAT_TEMPERATURE,
    CAT_AREA,
    CAT_VOLUME,
    CAT_WEIGHT,
    CAT_TIME,
    ENTER_VALUE,
)
from src.views.styles import (
    MAIN_WINDOW_STYLE,
    SIDEBAR_STYLE,
    SIDEBAR_BUTTON_STYLE,
    SIDEBAR_BUTTON_ACTIVE_STYLE,
    NEU_CARD_STYLE,
    INPUT_STYLE,
    COMBO_STYLE,
    SWAP_BUTTON_STYLE,
    SEARCH_INPUT_STYLE,
    TOOLBAR_BUTTON_STYLE,
    LABEL_STYLE,
    SECTION_TITLE_STYLE,
    HISTORY_PANEL_STYLE,
    HISTORY_ITEM_STYLE,
    CLEAR_BUTTON_STYLE,
    QUICK_REF_ITEM_STYLE,
    PREFERENCES_DIALOG_STYLE,
    SCROLLBAR_STYLE,
    ACCENT_BLUE,
    ACCENT_VIOLET,
    TEXT_WHITE,
    INSET_BG,
    BORDER_DIM,
    CARD_BG,
)

# Category translation key mapping
CATEGORY_I18N_KEYS = {
    "length": CAT_LENGTH,
    "temperature": CAT_TEMPERATURE,
    "area": CAT_AREA,
    "volume": CAT_VOLUME,
    "weight": CAT_WEIGHT,
    "time": CAT_TIME,
}


class PreferencesDialog(QDialog):
    """Dialog for application preferences (language selection)."""

    def __init__(self, prefs_vm: PreferencesViewModel, parent: QWidget = None) -> None:
        super().__init__(parent)
        self._prefs_vm = prefs_vm
        self.setWindowTitle(prefs_vm.get_text(PREFERENCES))
        self.setFixedSize(360, 200)
        self.setStyleSheet(PREFERENCES_DIALOG_STYLE)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel(self._prefs_vm.get_text(PREFERENCES))
        title.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
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


class DesktopWindow(QMainWindow):
    """Main desktop application window.

    Implements the neumorphic dark-mode design from the reference HTML
    with sidebar navigation, conversion panel, and history.
    """

    def __init__(
        self,
        converter_vm: ConverterViewModel,
        search_vm: SearchViewModel,
        prefs_vm: PreferencesViewModel,
    ) -> None:
        super().__init__()
        self._converter_vm = converter_vm
        self._search_vm = search_vm
        self._prefs_vm = prefs_vm
        self._sidebar_buttons: dict[str, QPushButton] = {}
        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.setInterval(300)
        self._search_timer.timeout.connect(self._execute_search)

        self.setWindowTitle("Unit Converter")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 800)
        self.setStyleSheet(MAIN_WINDOW_STYLE)

        self._setup_ui()
        self._connect_signals()
        self._update_sidebar_active()
        self._update_combos()

    def _setup_ui(self) -> None:
        """Build the complete desktop UI layout."""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        main_layout.addWidget(self._create_sidebar())

        # Main content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(32, 32, 32, 32)
        content_layout.setSpacing(24)

        content_layout.addWidget(self._create_header())
        content_layout.addWidget(self._create_conversion_panel())
        content_layout.addWidget(self._create_history_panel())

        scroll = QScrollArea()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet(
            f"QScrollArea {{ background: transparent; border: none; }} {SCROLLBAR_STYLE}"
        )
        main_layout.addWidget(scroll, 1)

    def _create_sidebar(self) -> QWidget:
        """Create the left sidebar with category navigation."""
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(SIDEBAR_STYLE)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(4)

        # Logo / Title
        header = QHBoxLayout()
        header.setSpacing(12)

        icon_label = QLabel("⚡")
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
            f"stop:0 {ACCENT_VIOLET}, stop:1 {ACCENT_BLUE}); "
            f"border-radius: 12px; font-size: 20px;"
        )
        header.addWidget(icon_label)

        self._title_label = QLabel(self._prefs_vm.get_text(APP_TITLE))
        self._title_label.setFont(QFont("Poppins", 14, QFont.Weight.Bold))
        self._title_label.setStyleSheet(f"color: {TEXT_WHITE};")
        header.addWidget(self._title_label)
        header.addStretch()

        layout.addLayout(header)
        layout.addSpacing(32)

        # Category navigation
        for category in self._converter_vm.categories:
            btn = QPushButton(f"  {category.icon}   {category.name}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(SIDEBAR_BUTTON_STYLE)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setFixedHeight(48)
            cat_id = category.id
            btn.clicked.connect(
                lambda checked, cid=cat_id: self._on_category_clicked(cid)
            )
            self._sidebar_buttons[category.id] = btn
            layout.addWidget(btn)

        layout.addStretch()
        return sidebar

    def _create_header(self) -> QWidget:
        """Create the top header with search bar and settings."""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # Search bar
        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText(
            self._prefs_vm.get_text(SEARCH_PLACEHOLDER)
        )
        self._search_input.setStyleSheet(SEARCH_INPUT_STYLE)
        self._search_input.setMaximumWidth(400)
        self._search_input.setFixedHeight(44)
        self._search_input.textChanged.connect(self._on_search_text_changed)
        self._search_input.returnPressed.connect(self._on_search_enter)
        layout.addWidget(self._search_input)

        layout.addStretch()

        # Settings button
        settings_btn = QPushButton("⚙")
        settings_btn.setStyleSheet(TOOLBAR_BUTTON_STYLE)
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.clicked.connect(self._open_preferences)
        layout.addWidget(settings_btn)

        return header

    def _create_conversion_panel(self) -> QWidget:
        """Create the main conversion card with from/to inputs."""
        card = QWidget()
        card.setObjectName("conversionCard")
        card.setStyleSheet(NEU_CARD_STYLE)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Category header
        cat_header = QHBoxLayout()
        self._category_icon = QLabel("")
        self._category_icon.setStyleSheet(f"font-size: 24px; color: {TEXT_WHITE};")
        cat_header.addWidget(self._category_icon)

        self._category_title = QLabel("")
        self._category_title.setFont(QFont("Poppins", 18, QFont.Weight.Bold))
        self._category_title.setStyleSheet(f"color: {TEXT_WHITE};")
        cat_header.addWidget(self._category_title)
        cat_header.addStretch()
        layout.addLayout(cat_header)

        # From / To columns
        columns = QHBoxLayout()
        columns.setSpacing(32)

        # FROM column
        from_col = QVBoxLayout()
        from_col.setSpacing(12)

        self._from_label = QLabel(self._prefs_vm.get_text(FROM_LABEL))
        self._from_label.setStyleSheet(LABEL_STYLE)
        from_col.addWidget(self._from_label)

        self._from_combo = QComboBox()
        self._from_combo.setStyleSheet(COMBO_STYLE)
        self._from_combo.currentIndexChanged.connect(self._on_from_unit_changed)
        from_col.addWidget(self._from_combo)

        self._from_input = QLineEdit("1")
        self._from_input.setStyleSheet(INPUT_STYLE)
        self._from_input.setPlaceholderText("0")
        self._from_input.textChanged.connect(self._on_from_value_changed)
        from_col.addWidget(self._from_input)

        columns.addLayout(from_col, 1)

        # TO column
        to_col = QVBoxLayout()
        to_col.setSpacing(12)

        self._to_label = QLabel(self._prefs_vm.get_text(TO_LABEL))
        self._to_label.setStyleSheet(LABEL_STYLE)
        to_col.addWidget(self._to_label)

        self._to_combo = QComboBox()
        self._to_combo.setStyleSheet(COMBO_STYLE)
        self._to_combo.currentIndexChanged.connect(self._on_to_unit_changed)
        to_col.addWidget(self._to_combo)

        self._to_input = QLineEdit()
        self._to_input.setStyleSheet(INPUT_STYLE)
        self._to_input.setReadOnly(True)
        to_col.addWidget(self._to_input)

        columns.addLayout(to_col, 1)
        layout.addLayout(columns)

        # Swap button
        swap_row = QHBoxLayout()
        swap_row.addStretch()
        self._swap_btn = QPushButton("⇄")
        self._swap_btn.setStyleSheet(SWAP_BUTTON_STYLE)
        self._swap_btn.setFont(QFont("Poppins", 18))
        self._swap_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._swap_btn.clicked.connect(self._on_swap_clicked)
        swap_row.addWidget(self._swap_btn)
        swap_row.addStretch()
        layout.addLayout(swap_row)

        # Quick Reference
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"color: {BORDER_DIM};")
        layout.addWidget(separator)

        self._quick_ref_label = QLabel(self._prefs_vm.get_text(QUICK_REFERENCE))
        self._quick_ref_label.setStyleSheet(SECTION_TITLE_STYLE)
        layout.addWidget(self._quick_ref_label)

        self._quick_ref_layout = QHBoxLayout()
        self._quick_ref_layout.setSpacing(16)
        layout.addLayout(self._quick_ref_layout)

        self._update_category_display()
        self._update_quick_reference()
        return card

    def _create_history_panel(self) -> QWidget:
        """Create the conversion history panel."""
        panel = QWidget()
        panel.setObjectName("historyPanel")
        panel.setStyleSheet(HISTORY_PANEL_STYLE)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        header = QHBoxLayout()
        self._history_title = QLabel(self._prefs_vm.get_text(CONVERSION_HISTORY))
        self._history_title.setFont(QFont("Poppins", 14, QFont.Weight.DemiBold))
        self._history_title.setStyleSheet(f"color: {TEXT_WHITE};")
        header.addWidget(self._history_title)
        header.addStretch()

        self._clear_btn = QPushButton(self._prefs_vm.get_text(CLEAR_ALL))
        self._clear_btn.setStyleSheet(CLEAR_BUTTON_STYLE)
        self._clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._clear_btn.clicked.connect(self._converter_vm.clear_history)
        header.addWidget(self._clear_btn)
        layout.addLayout(header)

        self._history_container = QVBoxLayout()
        self._history_container.setSpacing(8)
        layout.addLayout(self._history_container)

        self._no_history_label = QLabel(self._prefs_vm.get_text(NO_CONVERSIONS))
        self._no_history_label.setStyleSheet(
            f"color: rgba(255,255,255,0.5); font-size: 13px;"
        )
        self._history_container.addWidget(self._no_history_label)

        return panel

    def _connect_signals(self) -> None:
        """Connect ViewModel signals to View updates."""
        self._converter_vm.category_changed.connect(self._on_vm_category_changed)
        self._converter_vm.result_changed.connect(self._on_vm_result_changed)
        self._converter_vm.history_changed.connect(self._on_vm_history_changed)
        self._prefs_vm.language_changed.connect(self._on_language_changed)

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
        self._update_sidebar_active()
        self._update_combos()
        self._update_category_display()
        self._update_quick_reference()

    def _on_vm_result_changed(self, result: str) -> None:
        self._to_input.setText(result)

    def _on_vm_history_changed(self) -> None:
        self._update_history()

    def _on_language_changed(self, lang: str) -> None:
        self._update_all_texts()

    # --- UI update methods ---

    def _update_sidebar_active(self) -> None:
        """Highlight the active category in the sidebar."""
        for cat_id, btn in self._sidebar_buttons.items():
            if cat_id == self._converter_vm.current_category_id:
                btn.setStyleSheet(SIDEBAR_BUTTON_ACTIVE_STYLE)
            else:
                btn.setStyleSheet(SIDEBAR_BUTTON_STYLE)

    def _update_combos(self) -> None:
        """Refresh the from/to combo boxes with current category units."""
        category = self._converter_vm.current_category

        self._from_combo.blockSignals(True)
        self._to_combo.blockSignals(True)

        self._from_combo.clear()
        self._to_combo.clear()

        for unit in category.units:
            display = f"{unit.name} ({unit.symbol})"
            self._from_combo.addItem(display, unit.id)
            self._to_combo.addItem(display, unit.id)

        # Set current selections
        from_idx = self._from_combo.findData(self._converter_vm.from_unit_id)
        to_idx = self._to_combo.findData(self._converter_vm.to_unit_id)
        self._from_combo.setCurrentIndex(max(from_idx, 0))
        self._to_combo.setCurrentIndex(max(to_idx, 0))

        self._from_combo.blockSignals(False)
        self._to_combo.blockSignals(False)

    def _update_category_display(self) -> None:
        """Update the category icon and title in the conversion panel."""
        category = self._converter_vm.current_category
        self._category_icon.setText(category.icon)

        i18n_key = CATEGORY_I18N_KEYS.get(category.id, CAT_LENGTH)
        translated = self._prefs_vm.get_text(i18n_key)
        self._category_title.setText(f"{translated} Converter")

    def _update_quick_reference(self) -> None:
        """Update the quick reference table."""
        # Clear existing items
        while self._quick_ref_layout.count():
            item = self._quick_ref_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        category = self._converter_vm.current_category
        units = category.units
        if len(units) < 2:
            return

        from_unit = units[0]
        to_unit = units[1]

        for val in [1, 10, 100, 1000]:
            try:
                result = self._converter_vm.service.convert(
                    val,
                    self._converter_vm.current_category_id,
                    from_unit.id,
                    to_unit.id,
                )
                ref_widget = QWidget()
                ref_widget.setStyleSheet(QUICK_REF_ITEM_STYLE)
                ref_layout = QVBoxLayout(ref_widget)
                ref_layout.setContentsMargins(12, 12, 12, 12)
                ref_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                val_label = QLabel(f"{val} {from_unit.symbol}")
                val_label.setFont(QFont("Poppins", 14, QFont.Weight.Bold))
                val_label.setStyleSheet(f"color: {TEXT_WHITE}; border: none;")
                val_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                ref_layout.addWidget(val_label)

                res_label = QLabel(f"= {result.to_value:.6g} {to_unit.symbol}")
                res_label.setStyleSheet(
                    f"color: {ACCENT_BLUE}; font-size: 13px; border: none;"
                )
                res_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                ref_layout.addWidget(res_label)

                self._quick_ref_layout.addWidget(ref_widget)
            except (ValueError, ZeroDivisionError):
                pass

    def _update_history(self) -> None:
        """Refresh the history list from ViewModel data."""
        # Clear existing
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
            self._clear_btn.setVisible(False)
            return

        self._clear_btn.setVisible(True)

        for entry in history[:10]:
            item_widget = QWidget()
            item_widget.setStyleSheet(HISTORY_ITEM_STYLE)
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(16, 12, 16, 12)

            # Category icon
            cat = self._converter_vm.service.get_category(entry.category_id)
            icon_text = cat.icon if cat else ""
            icon_label = QLabel(icon_text)
            icon_label.setStyleSheet("font-size: 18px; border: none;")
            item_layout.addWidget(icon_label)

            text_label = QLabel(entry.display_string)
            text_label.setFont(QFont("Poppins", 12, QFont.Weight.Medium))
            text_label.setStyleSheet(f"color: {TEXT_WHITE}; border: none;")
            item_layout.addWidget(text_label)

            item_layout.addStretch()

            time_label = QLabel(entry.time_string)
            time_label.setStyleSheet(
                f"color: rgba(255,255,255,0.5); font-size: 12px; border: none;"
            )
            item_layout.addWidget(time_label)

            self._history_container.addWidget(item_widget)

    def _update_all_texts(self) -> None:
        """Refresh all translatable text elements."""
        self._title_label.setText(self._prefs_vm.get_text(APP_TITLE))
        self._from_label.setText(self._prefs_vm.get_text(FROM_LABEL))
        self._to_label.setText(self._prefs_vm.get_text(TO_LABEL))
        self._search_input.setPlaceholderText(
            self._prefs_vm.get_text(SEARCH_PLACEHOLDER)
        )
        self._quick_ref_label.setText(self._prefs_vm.get_text(QUICK_REFERENCE))
        self._history_title.setText(self._prefs_vm.get_text(CONVERSION_HISTORY))
        self._clear_btn.setText(self._prefs_vm.get_text(CLEAR_ALL))
        self._update_category_display()
        self.setWindowTitle(self._prefs_vm.get_text(APP_TITLE))

    def _open_preferences(self) -> None:
        """Open the preferences dialog."""
        dialog = PreferencesDialog(self._prefs_vm, self)
        dialog.exec()
