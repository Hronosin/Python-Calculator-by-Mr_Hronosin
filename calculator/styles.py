"""
Styles and button configurations for the calculator.
"""

from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize
from .config import THEMES, CURRENT_THEME

theme = THEMES[CURRENT_THEME]

BTN_STYLES = {
    "num": {
        "bg": theme['CARD_BG'], "hover": theme['CARD_HOVER'],
        "fg": theme['TEXT_WHITE'], "size": 14
    },
    "op": {
        "bg": "#1f2a4a", "hover": "#263560",
        "fg": theme['ACCENT_BLUE'], "size": 15
    },
    "fn": {
        "bg": "#1e1e2a", "hover": "#28283a",
        "fg": theme['TEXT_MUTED'], "size": 12
    },
    "mem": {
        "bg": "#2a2215", "hover": "#38300a",
        "fg": theme['ACCENT_AMBER'], "size": 12
    },
    "eq": {
        "bg": theme['ACCENT_BLUE'], "hover": "#3a6aee",
        "fg": "#ffffff", "size": 18
    },
    "clr": {
        "bg": "#2a1515", "hover": "#3a1a1a",
        "fg": theme['ACCENT_RED'], "size": 13
    },
    "const": {
        "bg": "#152a1e", "hover": "#1c3828",
        "fg": theme['ACCENT_GREEN'], "size": 13
    },
    "mode": {
        "bg": "#252530", "hover": "#303040",
        "fg": theme['TEXT_MUTED'], "size": 11
    },
}

def make_btn(label: str, kind: str, w: int = 1, h: int = 1) -> QPushButton:
    """Create a styled button."""
    s = BTN_STYLES[kind]
    btn = QPushButton(label)
    btn.setFont(QFont("Consolas", s["size"]))
    btn.setMinimumSize(QSize(52, 44))
    btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    bg, hov, fg = s["bg"], s["hover"], s["fg"]
    btn.setStyleSheet(f"""
        QPushButton {{
            background: {bg};
            color: {fg};
            border: 1px solid {theme['BORDER']};
            border-radius: 8px;
            padding: 2px;
        }}
        QPushButton:hover {{ background: {hov}; }}
        QPushButton:pressed {{ background: {theme['DARK_BG']}; }}
    """)
    return btn