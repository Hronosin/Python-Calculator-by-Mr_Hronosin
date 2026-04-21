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
    app.setPalette(palette)

    win = calc.EngCalc()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()