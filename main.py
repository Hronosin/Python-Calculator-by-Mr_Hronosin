"""
Инженерный калькулятор на PyQt5
Запуск: python main.py
Зависимости: pip install PyQt5
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
import engineering_calculator as calc

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    theme = calc.THEMES[calc.CURRENT_THEME]
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(theme['DARK_BG']))
    palette.setColor(QPalette.WindowText, QColor(theme['TEXT_WHITE']))
    palette.setColor(QPalette.Base, QColor(theme['DISPLAY_BG']))
    palette.setColor(QPalette.AlternateBase, QColor(theme['PANEL_BG']))
    palette.setColor(QPalette.ToolTipBase, QColor(theme['DISPLAY_BG']))
    palette.setColor(QPalette.ToolTipText, QColor(theme['TEXT_WHITE']))
    palette.setColor(QPalette.Text, QColor(theme['TEXT_WHITE']))
    palette.setColor(QPalette.Button, QColor(theme['CARD_BG']))
    palette.setColor(QPalette.ButtonText, QColor(theme['TEXT_WHITE']))
    palette.setColor(QPalette.Highlight, QColor(theme['ACCENT_BLUE']))
    palette.setColor(QPalette.HighlightedText, QColor(theme['TEXT_WHITE']))
    app.setPalette(palette)

    app.setStyleSheet(f"""
        QWidget {{ color: {theme['TEXT_WHITE']}; background-color: {theme['DARK_BG']}; }}
        QLineEdit, QTextEdit, QComboBox, QListWidget, QSpinBox, QDoubleSpinBox {{
            color: {theme['TEXT_WHITE']};
            background-color: {theme['DISPLAY_BG']};
            border: 1px solid {theme['BORDER']};
        }}
        QComboBox::drop-down {{ border-left: 1px solid {theme['BORDER']}; }}
        QComboBox QAbstractItemView {{
            background-color: {theme['DISPLAY_BG']};
            color: {theme['TEXT_WHITE']};
            selection-background-color: {theme['CARD_HOVER']};
            selection-color: {theme['TEXT_WHITE']};
        }}
        QLabel {{ color: {theme['TEXT_WHITE']}; }}
        QPushButton {{ color: {theme['TEXT_WHITE']}; }}
        QMenuBar, QMenu {{ background-color: {theme['PANEL_BG']}; color: {theme['TEXT_WHITE']}; }}
        QMenu::item:selected {{ background-color: {theme['CARD_HOVER']}; }}
    """)

    win = calc.EngCalc()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()