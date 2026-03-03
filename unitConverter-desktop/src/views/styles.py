"""Stylesheet constants matching the reference HTML design.

Desktop design: Neumorphism dark mode with sidebar.
Colors sourced from the reference index.html.
"""

# Color palette from reference design
NAVY_DARK = "#0F0C29"
PURPLE_MID = "#302B63"
PURPLE_LIGHT = "#24243e"
ACCENT_VIOLET = "#7F5AF0"
ACCENT_BLUE = "#6C63FF"
SIDEBAR_BG = "#16161F"
CARD_BG = "#1E1E2E"
INSET_BG = "#16161F"
TEXT_WHITE = "#FFFFFF"
TEXT_DIM = "rgba(255, 255, 255, 0.6)"
BORDER_DIM = "rgba(255, 255, 255, 0.1)"

MAIN_WINDOW_STYLE = f"""
    QMainWindow {{
        background-color: {NAVY_DARK};
    }}
"""

SIDEBAR_STYLE = f"""
    QWidget#sidebar {{
        background-color: {SIDEBAR_BG};
        border-right: 1px solid {BORDER_DIM};
    }}
"""

SIDEBAR_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: transparent;
        color: rgba(255, 255, 255, 0.7);
        border: none;
        border-radius: 12px;
        padding: 12px 16px;
        text-align: left;
        font-size: 14px;
        font-weight: 500;
    }}
    QPushButton:hover {{
        background-color: rgba(108, 99, 255, 0.08);
        color: {TEXT_WHITE};
    }}
"""

SIDEBAR_BUTTON_ACTIVE_STYLE = f"""
    QPushButton {{
        background-color: rgba(108, 99, 255, 0.1);
        color: {ACCENT_BLUE};
        border: none;
        border-left: 3px solid {ACCENT_BLUE};
        border-radius: 12px;
        padding: 12px 16px;
        text-align: left;
        font-size: 14px;
        font-weight: 600;
    }}
"""

NEU_CARD_STYLE = f"""
    QWidget#conversionCard {{
        background-color: {CARD_BG};
        border-radius: 24px;
        border: 1px solid {BORDER_DIM};
    }}
"""

NEU_INSET_STYLE = f"""
    background-color: {INSET_BG};
    border-radius: 12px;
    border: 1px solid {BORDER_DIM};
    color: {TEXT_WHITE};
    padding: 12px 16px;
    font-size: 14px;
"""

INPUT_STYLE = f"""
    QLineEdit {{
        background-color: {INSET_BG};
        border-radius: 12px;
        border: 1px solid {BORDER_DIM};
        color: {TEXT_WHITE};
        padding: 16px;
        font-size: 24px;
        font-weight: 700;
    }}
    QLineEdit:focus {{
        border-color: rgba(127, 90, 240, 0.5);
    }}
    QLineEdit[readOnly="true"] {{
        color: {ACCENT_BLUE};
    }}
"""

COMBO_STYLE = f"""
    QComboBox {{
        background-color: {INSET_BG};
        border-radius: 12px;
        border: 1px solid {BORDER_DIM};
        color: {TEXT_WHITE};
        padding: 12px 16px;
        font-size: 14px;
        font-weight: 500;
        min-height: 20px;
    }}
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid {ACCENT_BLUE};
        margin-right: 10px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {INSET_BG};
        color: {TEXT_WHITE};
        border: 1px solid {BORDER_DIM};
        border-radius: 8px;
        selection-background-color: rgba(108, 99, 255, 0.2);
        padding: 4px;
    }}
"""

SWAP_BUTTON_STYLE = f"""
    QPushButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #2A2A3E, stop:1 #1E1E2E);
        border: 1px solid {BORDER_DIM};
        border-radius: 28px;
        min-width: 56px;
        max-width: 56px;
        min-height: 56px;
        max-height: 56px;
    }}
    QPushButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #3A3A4E, stop:1 #2E2E3E);
    }}
    QPushButton:pressed {{
        background: {INSET_BG};
    }}
"""

SEARCH_INPUT_STYLE = f"""
    QLineEdit {{
        background-color: {INSET_BG};
        border-radius: 12px;
        border: 1px solid {BORDER_DIM};
        color: {TEXT_WHITE};
        padding: 12px 16px 12px 40px;
        font-size: 14px;
    }}
    QLineEdit:focus {{
        border-color: rgba(127, 90, 240, 0.5);
    }}
"""

TOOLBAR_BUTTON_STYLE = f"""
    QPushButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #2A2A3E, stop:1 #1E1E2E);
        border: 1px solid {BORDER_DIM};
        border-radius: 12px;
        min-width: 40px;
        max-width: 40px;
        min-height: 40px;
        max-height: 40px;
        color: {TEXT_WHITE};
        font-size: 16px;
    }}
    QPushButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #3A3A4E, stop:1 #2E2E3E);
    }}
"""

LABEL_STYLE = f"""
    QLabel {{
        color: {ACCENT_BLUE};
        font-size: 13px;
        font-weight: 600;
    }}
"""

SECTION_TITLE_STYLE = f"""
    QLabel {{
        color: {TEXT_DIM};
        font-size: 13px;
        font-weight: 600;
    }}
"""

HISTORY_PANEL_STYLE = f"""
    QWidget#historyPanel {{
        background-color: {CARD_BG};
        border-radius: 16px;
        border: 1px solid {BORDER_DIM};
    }}
"""

HISTORY_ITEM_STYLE = f"""
    QWidget {{
        background-color: {INSET_BG};
        border-radius: 12px;
        border: 1px solid {BORDER_DIM};
    }}
"""

CLEAR_BUTTON_STYLE = f"""
    QPushButton {{
        background: transparent;
        border: none;
        color: {ACCENT_BLUE};
        font-size: 13px;
        font-weight: 500;
    }}
    QPushButton:hover {{
        color: {ACCENT_VIOLET};
    }}
"""

QUICK_REF_ITEM_STYLE = f"""
    QWidget {{
        background-color: {INSET_BG};
        border-radius: 12px;
        border: 1px solid {BORDER_DIM};
        padding: 12px;
    }}
"""

PREFERENCES_DIALOG_STYLE = f"""
    QDialog {{
        background-color: {CARD_BG};
        border: 1px solid {BORDER_DIM};
    }}
    QLabel {{
        color: {TEXT_WHITE};
        font-size: 14px;
    }}
    QComboBox {{
        background-color: {INSET_BG};
        border-radius: 8px;
        border: 1px solid {BORDER_DIM};
        color: {TEXT_WHITE};
        padding: 8px 12px;
        font-size: 14px;
        min-height: 20px;
    }}
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid {ACCENT_BLUE};
        margin-right: 8px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {INSET_BG};
        color: {TEXT_WHITE};
        border: 1px solid {BORDER_DIM};
        selection-background-color: rgba(108, 99, 255, 0.2);
    }}
    QPushButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {ACCENT_VIOLET}, stop:1 {ACCENT_BLUE});
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 14px;
        font-weight: 600;
    }}
    QPushButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {ACCENT_BLUE}, stop:1 {ACCENT_VIOLET});
    }}
"""

SCROLLBAR_STYLE = f"""
    QScrollBar:vertical {{
        background: transparent;
        width: 6px;
        border-radius: 3px;
    }}
    QScrollBar::handle:vertical {{
        background: rgba(127, 90, 240, 0.3);
        border-radius: 3px;
        min-height: 20px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: rgba(127, 90, 240, 0.5);
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
    }}
"""
