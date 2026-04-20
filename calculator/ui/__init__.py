"""
📦 UI Module  
============

Пользовательский интерфейс калькулятора

Содержит:
- EngineeringCalculatorApp: Главное приложение
- Космический минимализм дизайн
- Полная функциональность: графики, производные, интегралы

Цветовая схема: COSMIC MINIMALISM
- Фон: #0a0e27 (глубокий космос)
- Акценты: Неоны (cyan, purple, pink, green)
"""

import tkinter as tk
from tkinter import Canvas, Scrollbar
import math

from calculator.core import evaluate
from calculator.tools import GraphGenerator, Derivative, Integral
from calculator.converters import CONVERTERS
from calculator.localization import Localizator
from calculator.history import HistoryManager
from calculator.utils import ImportTargetDialog, FileDialog, show_error, show_info


# =============================================================================
# ЦВЕТОВАЯ СХЕМА - COSMIC MINIMALISM
# =============================================================================

# ВАЖНО: Все цвета подобраны для минималистичного космического стиля

COLOR_BG_PRIMARY = "#0a0e27"      # Глубокий космос - основной фон
COLOR_BG_SECONDARY = "#0f1535"    # Тёмнее для кнопок
COLOR_ACCENT_CYAN = "#00d9ff"     # Неон циан - яркий акцент
COLOR_ACCENT_PURPLE = "#b026ff"   # Неон фиолетовый
COLOR_ACCENT_PINK = "#ff006e"     # Неон розовый
COLOR_ACCENT_GREEN = "#00ff88"    # Неон зелёный
COLOR_TEXT_PRIMARY = "#e0e0e0"    # Светлый текст
COLOR_TEXT_SECONDARY = "#a0a0a0"  # Приглушённый текст
COLOR_ERROR = "#ff4444"           # Ошибка красная
COLOR_SUCCESS = "#44ff44"         # Успех зелёная


# =============================================================================
# ГЛАВНОЕ ПРИЛОЖЕНИЕ
# =============================================================================

class EngineeringCalculatorApp(tk.Tk):
    """
    Главное окно приложения - Инженерный калькулятор
    
    Функциональность:
    - Базовые операции (+, -, *, /)
    - 36+ математических функций
    - Графики функций
    - Численное дифференцирование
    - Численное интегрирование
    - Преобразование единиц
    - История вычислений
    - Многоязычный интерфейс (УК, EN, RU)
    """
    
    def __init__(self):
        """Инициализировать приложение"""
        tk.Tk.__init__(self)
        
        # Свойства окна
        self.title("Engineering Calculator")
        self.geometry("900x700")
        self.resizable(True, True)
        self.configure(bg=COLOR_BG_PRIMARY)
        
        # Инициализируем компоненты
        self.expression = tk.StringVar(value="")
        self.language = tk.StringVar(value="uk")
        self.localizator = Localizator("uk")
        self.history_manager = HistoryManager()
        
        # Статус окна
        self.status_message = ""
        self.status_timer = None
        
        # Создаём интерфейс
        self._build_ui()
    
    def _translate(self, key: str, **kwargs) -> str:
        """Получить переведённый текст для UI."""
        return self.localizator.get(key, **kwargs)
    
    def _build_ui(self):
        """
        Построить весь интерфейс
        
        Структура:
        1. Верхний заголовок
        2. Поле ввода выражения
        3. Сетка кнопок операций и функций
        4. Панель инструментов
        5. История вычислений
        6. Статус-бар
        """
        # ===== МЕНЮ =====
        self._build_menu()
        
        # ===== ЗАГОЛОВОК =====
        self.title(self._translate("app_title"))
        header = tk.Frame(self, bg=COLOR_BG_PRIMARY)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        tk.Label(
            header,
            text=self._translate("calculator_header"),
            font=("Monaco", 16, "bold"),
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_BG_PRIMARY
        ).pack()
        
        # ===== ПОЛЕ ВВОДА =====
        input_frame = tk.Frame(self, bg=COLOR_BG_PRIMARY)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.display = tk.Text(
            input_frame,
            height=4,
            font=("Courier", 12),
            bg=COLOR_BG_SECONDARY,
            fg=COLOR_TEXT_PRIMARY,
            insertbackground=COLOR_ACCENT_CYAN,
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=15,
            pady=15
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        self.display.bind("<<Change>>", self._on_text_change)
        
        # Привязываем переменную к тексту
        def on_display_change(*args):
            current_text = self.display.get("1.0", "end-1c")
            if current_text != self.expression.get():
                self.expression.set(current_text)
        
        self.display.bind("<KeyRelease>", on_display_change)
        
        # ===== ГЛАВНАЯ ПАНЕЛЬ С КНОПКАМИ И ИСТОРИЕЙ =====
        main_panel = tk.Frame(self, bg=COLOR_BG_PRIMARY)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Левая часть - Кнопки
        self._build_buttons_panel(main_panel)
        
        # Правая часть - История
        self._build_history_panel(main_panel)
        
        # ===== СТАТУС БАР =====
        self._build_status_bar()
    
    def _build_menu(self):
        """Построить главное меню"""
        menubar = tk.Menu(self, bg=COLOR_BG_SECONDARY, fg=COLOR_TEXT_PRIMARY)
        self.config(menu=menubar)
        
        # МЕНЮ: Файл
        file_menu = tk.Menu(menubar, bg=COLOR_BG_SECONDARY, fg=COLOR_TEXT_PRIMARY)
        menubar.add_cascade(label=self.localizator.get("file"), menu=file_menu)
        
        file_menu.add_command(
            label=self.localizator.get("export"),
            command=self._export_history
        )
        file_menu.add_command(
            label=self.localizator.get("import"),
            command=self._import_history
        )
        file_menu.add_separator()
        file_menu.add_command(
            label=self.localizator.get("clear_history"),
            command=self._clear_history_prompt
        )
        file_menu.add_separator()
        file_menu.add_command(
            label=self.localizator.get("exit"),
            command=self.quit
        )
        
        # МЕНЮ: Язык
        lang_menu = tk.Menu(menubar, bg=COLOR_BG_SECONDARY, fg=COLOR_TEXT_PRIMARY)
        menubar.add_cascade(label=self.localizator.get("language"), menu=lang_menu)
        
        for lang_code in ["uk", "en", "ru"]:
            lang_menu.add_command(
                label=lang_code.upper(),
                command=lambda lc=lang_code: self._set_language(lc)
            )
    
    def _build_buttons_panel(self, parent):
        """
        Построить панель кнопок
        
        Содержит:
        - Основные операции
        - Функции
        - Инструменты (график, производная и т.д.)
        """
        button_frame = tk.Frame(parent, bg=COLOR_BG_PRIMARY)
        button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # РЯДЫ 1-2: Основные операции + функции
        rows = [
            # Ряд 1: Очистка + основные операции
            [
                ("C", COLOR_ACCENT_PINK, self._clear_display),
                ("DEL", COLOR_ACCENT_PINK, self._delete_char),
                ("÷", COLOR_ACCENT_CYAN, lambda: self._add_to_display("/")),
                ("×", COLOR_ACCENT_CYAN, lambda: self._add_to_display("*")),
            ],
            # Ряд 2: Цифры и операции
            [
                ("7", COLOR_ACCENT_GREEN, lambda: self._add_to_display("7")),
                ("8", COLOR_ACCENT_GREEN, lambda: self._add_to_display("8")),
                ("9", COLOR_ACCENT_GREEN, lambda: self._add_to_display("9")),
                ("−", COLOR_ACCENT_CYAN, lambda: self._add_to_display("-")),
            ],
            # Ряд 3
            [
                ("4", COLOR_ACCENT_GREEN, lambda: self._add_to_display("4")),
                ("5", COLOR_ACCENT_GREEN, lambda: self._add_to_display("5")),
                ("6", COLOR_ACCENT_GREEN, lambda: self._add_to_display("6")),
                ("+", COLOR_ACCENT_CYAN, lambda: self._add_to_display("+")),
            ],
            # Ряд 4
            [
                ("1", COLOR_ACCENT_GREEN, lambda: self._add_to_display("1")),
                ("2", COLOR_ACCENT_GREEN, lambda: self._add_to_display("2")),
                ("3", COLOR_ACCENT_GREEN, lambda: self._add_to_display("3")),
                ("(", COLOR_ACCENT_PURPLE, lambda: self._add_to_display("(")),
            ],
            # Ряд 5
            [
                ("0", COLOR_ACCENT_GREEN, lambda: self._add_to_display("0")),
                (".", COLOR_ACCENT_GREEN, lambda: self._add_to_display(".")),
                ("^", COLOR_ACCENT_PURPLE, lambda: self._add_to_display("^")),
                (")", COLOR_ACCENT_PURPLE, lambda: self._add_to_display(")")),
            ],
        ]
        
        # Рисуем строки кнопок операций
        for row_buttons in rows:
            row = tk.Frame(button_frame, bg=COLOR_BG_PRIMARY)
            row.pack(fill=tk.X, pady=4)
            
            for text, color, command in row_buttons:
                self._create_styled_button(
                    row, text, color, command
                ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2)
        
        # ФУНКЦИИ: Тригонометрия
        tk.Label(
            button_frame,
            text=self._translate("trigonometry_section"),
            font=("Monaco", 9, "bold"),
            fg=COLOR_ACCENT_PURPLE,
            bg=COLOR_BG_PRIMARY
        ).pack(pady=(15, 5))
        
        trig_functions = [
            ("sin", "sin("),
            ("cos", "cos("),
            ("tan", "tan("),
            ("asin", "asin("),
            ("acos", "acos("),
            ("atan", "atan("),
        ]
        
        trig_row = tk.Frame(button_frame, bg=COLOR_BG_PRIMARY)
        trig_row.pack(fill=tk.X, pady=2)
        
        for name, func in trig_functions:
            self._create_styled_button(
                trig_row, name, COLOR_ACCENT_PURPLE,
                lambda f=func: self._add_to_display(f)
            ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=1)
        
        # ФУНКЦИИ: Экспоненциальные и логарифмические
        tk.Label(
            button_frame,
            text=self._translate("exp_log_section"),
            font=("Monaco", 9, "bold"),
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_BG_PRIMARY
        ).pack(pady=(15, 5))
        
        exp_functions = [
            ("√", "sqrt("),
            ("ln", "ln("),
            ("log", "log("),
            ("e^x", "exp("),
            ("n!", "factorial("),
            ("i", "i"),
        ]
        
        exp_row = tk.Frame(button_frame, bg=COLOR_BG_PRIMARY)
        exp_row.pack(fill=tk.X, pady=2)
        
        for name, func in exp_functions:
            self._create_styled_button(
                exp_row, name, COLOR_ACCENT_CYAN,
                lambda f=func: self._add_to_display(f)
            ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=1)
        
        # ИНСТРУМЕНТЫ
        tk.Label(
            button_frame,
            text=self._translate("tools_section"),
            font=("Monaco", 9, "bold"),
            fg=COLOR_ACCENT_GREEN,
            bg=COLOR_BG_PRIMARY
        ).pack(pady=(15, 5))
        
        tools_row = tk.Frame(button_frame, bg=COLOR_BG_PRIMARY)
        tools_row.pack(fill=tk.X, pady=2)
        
        self._create_styled_button(
            tools_row,
            f"📊 {self._translate('plot')}",
            COLOR_ACCENT_GREEN,
            self._plot_graph
        ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=1)
        
        self._create_styled_button(
            tools_row,
            f"∂ {self._translate('derivative')}",
            COLOR_ACCENT_GREEN,
            self._calculate_derivative
        ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=1)
        
        self._create_styled_button(
            tools_row,
            f"∫ {self._translate('integral')}",
            COLOR_ACCENT_GREEN,
            self._calculate_integral
        ).pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=1)
        
        # КНОПКА ВЫЧИСЛЕНИЯ
        tk.Label(
            button_frame,
            text="",
            bg=COLOR_BG_PRIMARY
        ).pack(pady=5)
        
        self._create_styled_button(
            button_frame,
            self._translate("calculate_button"),
            COLOR_ACCENT_PINK,
            self._calculate
        ).pack(fill=tk.X, pady=5)
    
    def _build_history_panel(self, parent):
        """
        Построить панель истории вычислений
        
        Отображает последние вычисления (самые новые сверху)
        """
        history_frame = tk.Frame(parent, bg=COLOR_BG_PRIMARY)
        history_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        # Заголовок
        tk.Label(
            history_frame,
            text=f"📝 {self._translate('history_section')}",
            font=("Monaco", 10, "bold"),
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_BG_PRIMARY
        ).pack(pady=(0, 5))
        
        # Список с скроллингом
        scrollbar = Scrollbar(history_frame, bg=COLOR_BG_SECONDARY)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(
            history_frame,
            font=("Courier", 8),
            bg=COLOR_BG_SECONDARY,
            fg=COLOR_TEXT_PRIMARY,
            yscrollcommand=scrollbar.set,
            relief=tk.FLAT,
            highlightthickness=0,
            width=25,
            height=20
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.history_listbox.bind("<<ListboxSelect>>", self._on_history_select)
        
        scrollbar.config(command=self.history_listbox.yview)
    
    def _build_status_bar(self):
        """
        Построить статус-бар в нижней части
        
        Показывает сообщения о статусе (готовность, ошибки и т.д.)
        """
        self.status_bar = tk.Label(
            self,
            text=self._translate("ready"),
            font=("Monaco", 9),
            fg=COLOR_ACCENT_GREEN,
            bg=COLOR_BG_SECONDARY,
            anchor=tk.W,
            padx=10,
            pady=5
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def _create_styled_button(self, parent, text: str, color: str, command):
        """
        Создать стилизованную кнопку
        
        Args:
            parent: Родительское окно
            text: Текст на кнопке
            color: Цвет неона (hex)
            command: Функция при клике
        
        Returns:
            tk.Button: Созданная кнопка
        """
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Monaco", 9, "bold"),
            fg=color,
            bg=COLOR_BG_SECONDARY,
            activeforeground=COLOR_BG_PRIMARY,
            activebackground=color,
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        return btn
    
    # =========================================================================
    # ОБРАБОТЧИКИ СОБЫТИЙ
    # =========================================================================
    
    def _add_to_display(self, value: str):
        """
        Добавить значение в поле ввода
        
        Вставляет в позицию курсора, не в конец!
        
        Args:
            value: Значение для вставления
        """
        current_text = self.display.get("1.0", "end-1c")
        cursor_pos = self.display.index("insert")
        
        # Парсим позицию курсора
        try:
            line, col = cursor_pos.split(".")
            line, col = int(line) - 1, int(col)
            
            # Вычисляем абсолютную позицию
            pos = len("\n".join(current_text.split("\n")[:line])) + col
            if line > 0:
                pos += line  # Добавляем символы переноса
            
            # Вставляем в позицию
            new_text = current_text[:pos] + value + current_text[pos:]
        except:
            # Если ошибка - просто добавляем в конец
            new_text = current_text + value
        
        self.display.delete("1.0", tk.END)
        self.display.insert("1.0", new_text)
        self.expression.set(new_text)
    
    def _delete_char(self):
        """Удалить символ перед курсором"""
        current_text = self.display.get("1.0", "end-1c")
        cursor_pos = self.display.index("insert")
        
        try:
            line, col = cursor_pos.split(".")
            line, col = int(line) - 1, int(col)
            
            # Вычисляем абсолютную позицию
            pos = len("\n".join(current_text.split("\n")[:line])) + col
            if line > 0:
                pos += line
            
            # Удаляем символ перед курсором
            if pos > 0:
                new_text = current_text[:pos-1] + current_text[pos:]
            else:
                new_text = current_text
        except:
            # Удаляем последний символ
            new_text = current_text[:-1]
        
        self.display.delete("1.0", tk.END)
        self.display.insert("1.0", new_text)
        self.expression.set(new_text)
    
    def _clear_display(self):
        """Очистить поле ввода"""
        self.display.delete("1.0", tk.END)
        self.expression.set("")
    
    def _calculate(self):
        """
        Вычислить выражение и добавить в историю
        
        ГЛАВНЫЙ ОБРАБОТЧИК расчётов!
        """
        expression = self.expression.get().strip()
        
        if not expression:
            self._set_status(self._translate("empty_expression"), COLOR_ERROR)
            return
        
        try:
            self._set_status(self._translate("calculating"), COLOR_TEXT_SECONDARY)
            self.update()
            
            # Вычисляем результат
            result = evaluate(expression)
            
            # Форматируем результат
            if isinstance(result, complex):
                result_str = f'{result.real:.10g} + {result.imag:.10g}j'
            elif isinstance(result, float):
                result_str = f'{result:.10g}'
            else:
                result_str = str(result)
            
            # Отображаем результат
            self.display.delete("1.0", tk.END)
            self.display.insert("1.0", result_str)
            self.expression.set(result_str)
            
            # Добавляем в историю
            self.history_manager.add(expression, result)
            self._update_history_display()
            
            # Статус
            self._set_status(self._translate("ready"), COLOR_SUCCESS)
        
        except Exception as e:
            error_msg = str(e)
            self._set_status(f"✗ Помилка: {error_msg[:30]}", COLOR_ERROR)
            show_error("Ошибка", f"Не можемо обчислити:\\n{error_msg}")
    
    def _calculate_derivative(self):
        """
        Вычислить производную функции
        
        Спрашивает точку x для вычисления производной
        """
        expression = self.expression.get().strip()
        
        if not expression or "x" not in expression:
            show_error("Ошибка", "Введите выражение с переменной x")
            return
        
        try:
            # Получаем точку
            x_value = float(self._prompt_input("Точка x для производной:"))
            
            # Вычисляем производную
            derivative = Derivative.calculate(expression, x_value)
            
            # Отображаем результат
            result_text = f"f'({x_value}) = {derivative:.6f}"
            self.display.delete("1.0", tk.END)
            self.display.insert("1.0", result_text)
            
            self._set_status("✓ Производная вычислена", COLOR_SUCCESS)
        
        except Exception as e:
            show_error("Ошибка", f"Не удалось вычислить производную:\\n{e}")
    
    def _calculate_integral(self):
        """
        Вычислить определённый интеграл
        
        Спрашивает пределы интегрирования [a, b]
        """
        expression = self.expression.get().strip()
        
        if not expression or "x" not in expression:
            show_error("Ошибка", "Введите выражение с переменной x")
            return
        
        try:
            # Получаем пределы
            a = float(self._prompt_input("Нижний предел a:"))
            b = float(self._prompt_input("Верхний предел b:"))
            
            # Вычисляем интеграл
            integral = Integral.calculate(expression, a, b)
            
            # Отображаем результат
            result_text = f"∫[{a},{b}] f(x)dx = {integral:.6f}"
            self.display.delete("1.0", tk.END)
            self.display.insert("1.0", result_text)
            
            self._set_status("✓ Интеграл вычислен", COLOR_SUCCESS)
        
        except Exception as e:
            show_error("Ошибка", f"Не удалось вычислить интеграл:\\n{e}")
    
    def _plot_graph(self):
        """
        Построить график функции
        
        Создаёт новое окно с графиком функции
        """
        expression = self.expression.get().strip()
        
        if not expression or "x" not in expression:
            show_error("Ошибка", "Введите выражение с переменной x")
            return
        
        try:
            # Получаем диапазон
            x_min = float(self._prompt_input("X min:"))
            x_max = float(self._prompt_input("X max:"))
            
            if x_min >= x_max:
                show_error("Ошибка", "X min должен быть < X max")
                return
            
            # Генерируем точки графика
            xs, ys = GraphGenerator.generate_points(expression, x_min, x_max)
            
            # Создаём окно графика
            plot_window = tk.Toplevel(self)
            plot_window.title(f"График: {expression}")
            plot_window.geometry("600x500")
            
            # Рисуем график на Canvas
            canvas = Canvas(
                plot_window,
                bg=COLOR_BG_PRIMARY,
                highlightthickness=0
            )
            canvas.pack(fill=tk.BOTH, expand=True)
            
            # Параметры отрисовки
            width = canvas.winfo_width() or 600
            height = canvas.winfo_height() or 500
            
            canvas.update()
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            # Поля графика
            margin = 40
            plot_width = width - 2 * margin
            plot_height = height - 2 * margin
            
            # Находим y min/max для масштабирования
            y_values = [y for y in ys if y is not None]
            if y_values:
                y_min = min(y_values)
                y_max = max(y_values)
                if y_min == y_max:
                    y_min -= 1
                    y_max += 1
            else:
                y_min, y_max = 0, 1
            
            # Рисуем оси
            canvas.create_line(
                margin, height - margin,
                width - margin, height - margin,
                fill=COLOR_ACCENT_CYAN, width=2
            )
            canvas.create_line(
                margin, margin,
                margin, height - margin,
                fill=COLOR_ACCENT_CYAN, width=2
            )
            
            # Рисуем график
            prev_x_pixel = None
            prev_y_pixel = None
            
            for x, y in zip(xs, ys):
                if y is None:
                    prev_x_pixel = None
                    prev_y_pixel = None
                    continue
                
                # Масштабируем координаты
                x_pixel = margin + (x - x_min) / (x_max - x_min) * plot_width
                y_pixel = height - margin - (y - y_min) / (y_max - y_min) * plot_height
                
                if prev_x_pixel is not None:
                    canvas.create_line(
                        prev_x_pixel, prev_y_pixel,
                        x_pixel, y_pixel,
                        fill=COLOR_ACCENT_GREEN, width=2
                    )
                
                prev_x_pixel = x_pixel
                prev_y_pixel = y_pixel
            
            self._set_status("✓ График построен", COLOR_SUCCESS)
        
        except Exception as e:
            show_error("Ошибка", f"Не удалось построить график:\\n{e}")
    
    def _on_history_select(self, event):
        """Обработчик клика по элементу истории"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            record = self.history_manager.get_all()[index]
            
            # Вставляем выражение в поле ввода
            self.display.delete("1.0", tk.END)
            self.display.insert("1.0", record["expression"])
            self.expression.set(record["expression"])
    
    def _update_history_display(self):
        """Обновить отображение истории"""
        self.history_listbox.delete(0, tk.END)
        
        for record in self.history_manager.get_all():
            expr = record["expression"]
            result = record["result"]
            
            # Форматируем для отображения
            if len(expr) > 20:
                expr = expr[:17] + "..."
            
            item_text = f"{expr} = {result}"
            self.history_listbox.insert(0, item_text)
    
    def _export_history(self):
        """Экспортировать историю в JSON"""
        filepath = FileDialog.save_file()
        if filepath:
            try:
                self.history_manager.save_to_file(filepath)
                show_info("Успех", f"История сохранена в:\\n{filepath}")
            except Exception as e:
                show_error("Ошибка", f"Не удалось сохранить историю:\\n{e}")
    
    def _import_history(self):
        """Импортировать историю из JSON"""
        filepath = FileDialog.open_file()
        if filepath:
            try:
                # Спрашиваем: заменить или добавить
                dialog = ImportTargetDialog(
                    self,
                    title="Импорт истории",
                    message="Заменить существующую историю или добавить?",
                    texts={
                        "replace": "Заменить",
                        "append": "Добавить",
                        "cancel": "Отмена"
                    }
                )
                
                if dialog.result == "replace":
                    self.history_manager.clear()
                    self.history_manager.load_from_file(filepath)
                elif dialog.result == "append":
                    self.history_manager.load_from_file(filepath, append=True)
                
                self._update_history_display()
                show_info("Успех", "История импортирована")
            
            except Exception as e:
                show_error("Ошибка", f"Не удалось загрузить историю:\\n{e}")
    
    def _clear_history_prompt(self):
        """Спросить перед очисткой истории"""
        if tk.messagebox.askyesno("Очистить историю?", 
                                   "Вы уверены? Это действие необратимо"):
            self.history_manager.clear()
            self._update_history_display()
            self._set_status("✓ История очищена", COLOR_SUCCESS)
    
    def _set_language(self, lang_code: str):
        """Установить язык интерфейса"""
        self.localizator.set_language(lang_code)
        self.language.set(lang_code)
        # Перестраиваем меню (основной интерфейс не меняется)
        self._build_menu()
    
    def _set_status(self, message: str, color: str = COLOR_TEXT_PRIMARY):
        """
        Установить сообщение в статус-баре
        
        Автоматически исчезает через 2 секунды
        """
        self.status_bar.config(text=message, fg=color)
        
        # Отменяем старый таймер если есть
        if self.status_timer:
            self.after_cancel(self.status_timer)
        
        # Устанавливаем новый таймер
        self.status_timer = self.after(
            2000,
            lambda: self.status_bar.config(text="✓ Готово", fg=COLOR_SUCCESS)
        )
    
    def _on_text_change(self, event):
        """Обработчик изменения текста в поле ввода"""
        pass
    
    @staticmethod
    def _prompt_input(prompt_text: str):
        """
        Простой диалог для ввода текста
        
        Args:
            prompt_text: Текст приглашения
        
        Returns:
            str: Введённый текст или None если отменено
        """
        # Это функция-заглушка, в реальном приложении используется
        # tk.simpledialog.askstring() но без импорта
        root = tk.Tk()
        root.withdraw()
        
        from tkinter.simpledialog import askstring
        result = askstring("Input", prompt_text)
        
        root.destroy()
        return result
