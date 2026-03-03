"""Stylesheet constants for the mobile glassmorphism design.

Colors sourced from the reference index.html mobile view.
Glassmorphism: translucent backgrounds with blur effect.
"""

# Color palette
NAVY_DARK = "#0F0C29"
PURPLE_MID = "#302B63"
PURPLE_LIGHT = "#24243e"
ACCENT_VIOLET = "#7F5AF0"
ACCENT_BLUE = "#6C63FF"
TEXT_WHITE = "#FFFFFF"
GLASS_BG = "rgba(255, 255, 255, 8%)"
GLASS_BORDER = "rgba(255, 255, 255, 15%)"
GLASS_INPUT_BG = "rgba(255, 255, 255, 5%)"
GLASS_INPUT_BORDER = "rgba(255, 255, 255, 10%)"

MOBILE_WINDOW_STYLE = f"""
    QMainWindow {{
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 {NAVY_DARK},
            stop:0.5 {PURPLE_MID},
            stop:1 {PURPLE_LIGHT}
        );
    }}
"""

GLASS_CARD_STYLE = f"""
    QWidget#glassCard {{
        background-color: {GLASS_BG};
        border: 1px solid {GLASS_BORDER};
        border-radius: 24px;
    }}
"""

GLASS_INPUT_STYLE = f"""
    QLineEdit {{
        background-color: {GLASS_INPUT_BG};
        border: 1px solid {GLASS_INPUT_BORDER};
        border-radius: 16px;
        color: {TEXT_WHITE};
        padding: 16px;
        font-size: 18px;
        font-weight: 600;
    }}
    QLineEdit:focus {{
        border-color: rgba(127, 90, 240, 0.5);
    }}
"""

GLASS_COMBO_STYLE = f"""
    QComboBox {{
        background-color: {GLASS_INPUT_BG};
        border: 1px solid {GLASS_INPUT_BORDER};
        border-radius: 16px;
        color: {TEXT_WHITE};
        padding: 16px;
        font-size: 14px;
        font-weight: 500;
        min-height: 20px;
    }}
    QComboBox::drop-down {{
        border: none;
        width: 28px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid {TEXT_WHITE};
        margin-right: 10px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {PURPLE_LIGHT};
        color: {TEXT_WHITE};
        border: 1px solid {GLASS_BORDER};
        border-radius: 8px;
        selection-background-color: rgba(127, 90, 240, 0.3);
        padding: 4px;
    }}
"""

PILL_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {GLASS_BG};
        border: 1px solid {GLASS_BORDER};
        border-radius: 20px;
        color: {TEXT_WHITE};
        padding: 10px 16px;
        font-size: 13px;
        font-weight: 500;
    }}
"""

PILL_BUTTON_ACTIVE_STYLE = f"""
    QPushButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {ACCENT_VIOLET}, stop:1 {ACCENT_BLUE});
        border: none;
        border-radius: 20px;
        color: {TEXT_WHITE};
        padding: 10px 16px;
        font-size: 13px;
        font-weight: 500;
    }}
"""

SWAP_BUTTON_MOBILE_STYLE = f"""
    QPushButton {{
        background-color: {ACCENT_VIOLET};
        border: none;
        border-radius: 24px;
        min-width: 48px;
        max-width: 48px;
        min-height: 48px;
        max-height: 48px;
        color: {TEXT_WHITE};
        font-size: 18px;
    }}
    QPushButton:hover {{
        background-color: {ACCENT_BLUE};
    }}
"""

BOTTOM_NAV_STYLE = f"""
    QWidget#bottomNav {{
        background-color: {GLASS_BG};
        border-top: 1px solid {GLASS_INPUT_BORDER};
    }}
"""

NAV_BUTTON_STYLE = f"""
    QPushButton {{
        background: transparent;
        border: none;
        color: rgba(255, 255, 255, 0.6);
        font-size: 11px;
        padding: 8px;
    }}
"""

NAV_BUTTON_ACTIVE_STYLE = f"""
    QPushButton {{
        background: transparent;
        border: none;
        color: {ACCENT_VIOLET};
        font-size: 11px;
        padding: 8px;
    }}
"""

SEARCH_INPUT_MOBILE_STYLE = f"""
    QLineEdit {{
        background-color: {GLASS_INPUT_BG};
        border: 1px solid {GLASS_INPUT_BORDER};
        border-radius: 16px;
        color: {TEXT_WHITE};
        padding: 12px 16px 12px 40px;
        font-size: 14px;
    }}
    QLineEdit:focus {{
        border-color: rgba(127, 90, 240, 0.5);
    }}
"""

HISTORY_CARD_STYLE = f"""
    QWidget#historyCard {{
        background-color: {GLASS_BG};
        border: 1px solid {GLASS_BORDER};
        border-radius: 16px;
    }}
"""

PREFERENCES_DIALOG_MOBILE_STYLE = f"""
    QDialog {{
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 {NAVY_DARK},
            stop:1 {PURPLE_LIGHT}
        );
    }}
    QLabel {{
        color: {TEXT_WHITE};
        font-size: 14px;
    }}
    QComboBox {{
        background-color: {GLASS_INPUT_BG};
        border: 1px solid {GLASS_INPUT_BORDER};
        border-radius: 12px;
        color: {TEXT_WHITE};
        padding: 10px 14px;
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
        border-top: 5px solid {ACCENT_VIOLET};
        margin-right: 8px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {PURPLE_LIGHT};
        color: {TEXT_WHITE};
        border: 1px solid {GLASS_BORDER};
        selection-background-color: rgba(127, 90, 240, 0.3);
    }}
    QPushButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {ACCENT_VIOLET}, stop:1 {ACCENT_BLUE});
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 14px;
        font-weight: 600;
    }}
"""

SCROLLBAR_MOBILE_STYLE = """
    QScrollBar:vertical {
        background: transparent;
        width: 4px;
    }
    QScrollBar::handle:vertical {
        background: rgba(127, 90, 240, 0.3);
        border-radius: 2px;
        min-height: 20px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
"""
