'''
Starting Engineering Calculator
=================================

Main entry point for the application

Запуск:
    python main.py
'''

# Прямой импорт чтобы избежать проблем с модулями
import sys
from pathlib import Path

# Добавляем папку проекта в путь поиска
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Теперь импортируем UI
from calculator.ui import EngineeringCalculatorApp


def main():
    '''Run the calculator application'''
    app = EngineeringCalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
