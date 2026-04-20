import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

from calculator_core import evaluate
from dialogs import ImportTargetDialog
from history_manager import HistoryManager

TRANSLATIONS = {
    "uk": {
        "title": "Інженерний калькулятор",
        "info": "Enter = обчислити · Ctrl+A = виділити · Ctrl+C = копіювати · Del = видалити символ",
        "help": "Подвійний клік = вставити вираз · Перетащення = переміщення",
        "file_menu": "Файл",
        "language_menu": "Мова",
        "import_history": "Імпортувати історію JSON...",
        "export_history": "Експортувати історію JSON...",
        "clear_history": "Очистити історію",
        "exit": "Вийти",
        "history_title": "Історія",
        "no_history": "Немає записів історії для експорту.",
        "empty_expression": "Введіть вираз",
        "calculated": "✓ Скопійовано",
        "copied": "✓ В буфер обміну",
        "copy_empty": "Немає тексту",
        "history_cleared": "✓ Історія очищена",
        "imported": "✓ Імпортовано {count} записів",
        "exported": "✓ Експортовано",
        "error_calculate": "✗ Помилка:\n{error}",
        "error_generic": "✗ Помилка:\n{error}",
        "plot_title": "Графік",
        "plot_error": "✗ Графік:\n{error}",
        "plot_no_x": "Потрібна змінна x",
        "derivative_prompt": "x для похідної:",
        "derivative_result": "d/dx(x={x}) = {result}",
        "integral_prompt": "Межі (0,5):",
        "integral_result": "∫({start}→{end}) = {result}",
        "invalid_range": "Невірні межи",
        "import_prompt": "Дія імпорту:",
        "import_append": "Додати",
        "import_replace": "Замінити",
        "import_title": "Імпорт",
        "conversion_help": "Конвертація:\nkm_to_m, m_to_km, mi_to_km, km_to_mi\nc_to_f, f_to_c, c_to_k, k_to_c\ndeg_to_rad, rad_to_deg",
    },
    "en": {
        "title": "Engineering Calculator",
        "info": "Enter = calculate · Ctrl+A = select · Ctrl+C = copy · Del = delete",
        "help": "Double-click = restore · Drag = move",
        "file_menu": "File",
        "language_menu": "Language",
        "import_history": "Import history JSON...",
        "export_history": "Export history JSON...",
        "clear_history": "Clear history",
        "exit": "Exit",
        "history_title": "History",
        "no_history": "No history records.",
        "empty_expression": "Enter expression",
        "calculated": "✓ Copied",
        "copied": "✓ To clipboard",
        "copy_empty": "Nothing to copy",
        "history_cleared": "✓ History cleared",
        "imported": "✓ Imported {count} records",
        "exported": "✓ Exported",
        "error_calculate": "✗ Error:\n{error}",
        "error_generic": "✗ Error:\n{error}",
        "plot_title": "Plot",
        "plot_error": "✗ Plot:\n{error}",
        "plot_no_x": "Need variable x",
        "derivative_prompt": "x for derivative:",
        "derivative_result": "d/dx(x={x}) = {result}",
        "integral_prompt": "Bounds (0,5):",
        "integral_result": "∫({start}→{end}) = {result}",
        "invalid_range": "Invalid bounds",
        "import_prompt": "Import action:",
        "import_append": "Append",
        "import_replace": "Replace",
        "import_title": "Import",
        "conversion_help": "Conversions:\nkm_to_m, m_to_km, mi_to_km, km_to_mi\nc_to_f, f_to_c, c_to_k, k_to_c\ndeg_to_rad, rad_to_deg",
    },
    "ru": {
        "title": "Инженерный калькулятор",
        "info": "Enter = вычислить · Ctrl+A = выделить · Ctrl+C = копировать · Del = удалить",
        "help": "Двойной клик = восстановить · Перетащить = переместить",
        "file_menu": "Файл",
        "language_menu": "Язык",
        "import_history": "Импортировать историю JSON...",
        "export_history": "Экспортировать историю JSON...",
        "clear_history": "Очистить историю",
        "exit": "Выход",
        "history_title": "История",
        "no_history": "Нет записей истории",
        "empty_expression": "Введите выражение",
        "calculated": "✓ Скопировано",
        "copied": "✓ В буфер обмена",
        "copy_empty": "Нечего копировать",
        "history_cleared": "✓ История очищена",
        "imported": "✓ Импортировано {count} записей",
        "exported": "✓ Экспортировано",
        "error_calculate": "✗ Ошибка:\n{error}",
        "error_generic": "✗ Ошибка:\n{error}",
        "plot_title": "График",
        "plot_error": "✗ График:\n{error}",
        "plot_no_x": "Нужна переменная x",
        "derivative_prompt": "x для производной:",
        "derivative_result": "d/dx(x={x}) = {result}",
        "integral_prompt": "Границы (0,5):",
        "integral_result": "∫({start}→{end}) = {result}",
        "invalid_range": "Неверные границы",
        "import_prompt": "Действие импорта:",
        "import_append": "Добавить",
        "import_replace": "Заменить",
        "import_title": "Импорт",
        "conversion_help": "Конвертация:\nkm_to_m, m_to_km, mi_to_km, km_to_mi\nc_to_f, f_to_c, c_to_k, k_to_c\ndeg_to_rad, rad_to_deg",
    },
}


class EngineeringCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_language = "uk"
        self.title(TRANSLATIONS[self.current_language]["title"])
        
        # Космический дизайн - тёмные цвета
        self.BG_PRIMARY = "#0a0e27"      # Глубокий космос
        self.BG_SECONDARY = "#1a1f3a"    # Более светлый космос
        self.BG_ACCENT = "#2d3561"       # Акцент
        self.FG_PRIMARY = "#e0e6ff"      # Светлый текст
        self.FG_SECONDARY = "#7c8aff"    # Вторичный цвет
        self.ACCENT_CYAN = "#00d9ff"     # Циановый неон
        self.ACCENT_PURPLE = "#b026ff"   # Фиолетовый неон
        self.ACCENT_PINK = "#ff006e"     # Розовый неон
        self.ACCENT_GREEN = "#00ff88"    # Зелёный неон
        
        self.configure(bg=self.BG_PRIMARY)
        self.resizable(False, False)
        self.expression = tk.StringVar()
        self.history_manager = HistoryManager()
        self._build_ui()
        self._bind_keyboard()
        
        # Позиционирование окна в центре экрана
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

    def _t(self, key: str, **kwargs) -> str:
        return TRANSLATIONS[self.current_language][key].format(**kwargs)

    def _create_styled_button(self, parent, text, command, color_scheme="default", width=8):
        """Создаёт стилизованную кнопку космического стиля"""
        schemes = {
            "default": (self.BG_SECONDARY, self.FG_PRIMARY),
            "operator": (self.ACCENT_PURPLE, self.FG_PRIMARY),
            "function": (self.ACCENT_CYAN, self.BG_PRIMARY),
            "special": (self.ACCENT_GREEN, self.BG_PRIMARY),
            "equals": (self.ACCENT_PINK, self.FG_PRIMARY),
            "delete": (self.ACCENT_PINK, self.FG_PRIMARY),
        }
        bg, fg = schemes.get(color_scheme, schemes["default"])
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=self.ACCENT_CYAN,
            activeforeground=self.BG_PRIMARY,
            font=("SF Mono", 12, "bold"),
            bd=0,
            relief="flat",
            width=width,
            height=2,
            cursor="hand2",
            highlightthickness=0,
        )
        return btn

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Заголовок с космическим стилем
        header_frame = tk.Frame(self, bg=self.BG_PRIMARY, height=40)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        header_frame.grid_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="◆ " + self._t("title") + " ◆",
            bg=self.BG_PRIMARY,
            fg=self.ACCENT_CYAN,
            font=("SF Mono", 14, "bold"),
        )
        title_label.pack(side="left", padx=16, pady=8)

        # Основной контейнер
        main_container = tk.Frame(self, bg=self.BG_PRIMARY)
        main_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=12, pady=12)

        # Левая часть - вввод и кнопки
        left_panel = tk.Frame(main_container, bg=self.BG_PRIMARY)
        left_panel.pack(side="left", fill="both", expand=True)

        # Поле ввода с информацией
        input_frame = tk.Frame(left_panel, bg=self.BG_SECONDARY, relief="flat", bd=2, highlightthickness=2, highlightbackground=self.ACCENT_CYAN)
        input_frame.pack(fill="x", pady=(0, 8))

        self.display = tk.Entry(
            input_frame,
            textvariable=self.expression,
            font=("SF Mono", 18, "bold"),
            bg=self.BG_SECONDARY,
            fg=self.ACCENT_CYAN,
            insertbackground=self.ACCENT_GREEN,
            bd=0,
            relief="flat",
            justify="right",
            highlightthickness=0,
        )
        self.display.pack(fill="x", padx=12, pady=10, ipady=8)
        self.display.focus()

        # Строка с подсказкой
        hint_label = tk.Label(
            input_frame,
            text=self._t("info"),
            bg=self.BG_SECONDARY,
            fg=self.FG_SECONDARY,
            font=("SF Mono", 8),
            justify="left",
        )
        hint_label.pack(fill="x", padx=12, pady=(0, 8))
        self.hint_label = hint_label

        # Кнопки управления
        control_frame = tk.Frame(left_panel, bg=self.BG_PRIMARY)
        control_frame.pack(fill="x", pady=(0, 8))

        btn_clear = self._create_styled_button(control_frame, "⊘ Clear", lambda: self.on_button_press('C'), "delete", width=15)
        btn_clear.pack(side="left", padx=2)

        btn_del = self._create_styled_button(control_frame, "← DEL", lambda: self.on_button_press('DEL'), "delete", width=15)
        btn_del.pack(side="left", padx=2)

        # Сетка кнопок калькулятора
        button_frame = tk.Frame(left_panel, bg=self.BG_PRIMARY)
        button_frame.pack(fill="both", expand=True, pady=(0, 8))

        button_map = [
            [("(", "default"), (")", "default"), ("/", "operator"), ("*", "operator"), ("sqrt", "function"), ("^", "operator")],
            [("7", "default"), ("8", "default"), ("9", "default"), ("-", "operator"), ("log", "function"), ("ln", "function")],
            [("4", "default"), ("5", "default"), ("6", "default"), ("+", "operator"), ("exp", "function"), ("root", "function")],
            [("1", "default"), ("2", "default"), ("3", "default"), (".", "default"), ("sin", "function"), ("cos", "function")],
            [("0", "default"), ("Ans", "special"), (".", "default"), ("i", "function"), ("tan", "function"), ("abs", "function")],
            [("pi", "function"), ("e", "function"), ("fact", "function"), ("=", "equals"), ("d/dx", "special"), ("∫", "special")],
            [("Plot", "special"), ("Conv", "special"), ("Import", "special"), ("Export", "special"), ("History", "special"), ("Copy", "special")],
        ]

        for row_idx, row in enumerate(button_map):
            for col_idx, (text, style) in enumerate(row):
                btn_cmd = lambda t=text, s=lambda t=text: self.on_button_press(t) if t not in ("=", "Import", "Export", "History", "Copy", "Plot", "d/dx", "∫", "Conv") else self._special_action(t): s()
                btn = self._create_styled_button(button_frame, text, btn_cmd, style, width=7)
                btn.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky="nsew")

        # Правая панель - история
        right_panel = tk.Frame(main_container, bg=self.BG_SECONDARY, relief="flat", bd=2, highlightthickness=2, highlightbackground=self.ACCENT_PURPLE)
        right_panel.pack(side="right", fill="both", padx=(8, 0), ipadx=8, ipady=8)
        right_panel.pack_propagate(False)
        right_panel.configure(width=320)

        history_header = tk.Label(
            right_panel,
            text="▣ " + self._t("history_title"),
            bg=self.BG_SECONDARY,
            fg=self.ACCENT_PURPLE,
            font=("SF Mono", 12, "bold"),
        )
        history_header.pack(fill="x", pady=(0, 8))
        self.history_title_label = history_header

        self.history_list = tk.Listbox(
            right_panel,
            width=44,
            height=28,
            bg=self.BG_PRIMARY,
            fg=self.ACCENT_GREEN,
            selectbackground=self.ACCENT_PURPLE,
            selectforeground=self.FG_PRIMARY,
            font=("SF Mono", 9),
            bd=0,
            relief="flat",
            highlightthickness=0,
        )
        self.history_list.pack(side="left", fill="both", expand=True)
        self.history_list.bind("<Double-Button-1>", self._on_history_double_click)

        scrollbar = tk.Scrollbar(
            right_panel,
            orient="vertical",
            command=self.history_list.yview,
            bg=self.BG_SECONDARY,
            activebackground=self.ACCENT_CYAN,
            troughcolor=self.BG_PRIMARY,
        )
        scrollbar.pack(side="right", fill="y")
        self.history_list.config(yscrollcommand=scrollbar.set)

        # Нижний статус-бар
        status_frame = tk.Frame(self, bg=self.BG_PRIMARY, height=30)
        status_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        status_frame.grid_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text=self._t("help"),
            bg=self.BG_PRIMARY,
            fg=self.FG_SECONDARY,
            font=("SF Mono", 8),
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=16, pady=6)

        self.config(menu=self._build_menu())
        self.geometry("1100x700")

    def _build_menu(self):
        menu_bar = tk.Menu(self, bg=self.BG_SECONDARY, fg=self.FG_PRIMARY, activebackground=self.ACCENT_PURPLE, activeforeground=self.FG_PRIMARY)
        
        file_menu = tk.Menu(menu_bar, bg=self.BG_SECONDARY, fg=self.FG_PRIMARY, activebackground=self.ACCENT_PURPLE, activeforeground=self.FG_PRIMARY)
        file_menu.add_command(label=self._t("import_history"), command=self.import_history_json)
        file_menu.add_command(label=self._t("export_history"), command=self.export_history_json)
        file_menu.add_command(label=self._t("clear_history"), command=self.clear_history)
        file_menu.add_separator()
        file_menu.add_command(label=self._t("exit"), command=self.quit)
        menu_bar.add_cascade(label=self._t("file_menu"), menu=file_menu)

        language_menu = tk.Menu(menu_bar, bg=self.BG_SECONDARY, fg=self.FG_PRIMARY, activebackground=self.ACCENT_PURPLE, activeforeground=self.FG_PRIMARY)
        language_menu.add_command(label="English", command=lambda: self.set_language("en"))
        language_menu.add_command(label="Українська", command=lambda: self.set_language("uk"))
        language_menu.add_command(label="Русский", command=lambda: self.set_language("ru"))
        menu_bar.add_cascade(label=self._t("language_menu"), menu=language_menu)
        
        return menu_bar

    def _bind_keyboard(self):
        self.bind('<Return>', lambda event: self.calculate())
        self.bind('<Escape>', lambda event: self.on_button_press('C'))
        self.bind('<BackSpace>', lambda event: self.on_button_press('DEL'))
        self.bind('<Delete>', lambda event: self.on_button_press('DEL'))
        self.bind('<Control-o>', lambda event: self.import_history_json())
        self.bind('<Control-e>', lambda event: self.export_history_json())
        self.bind('<Control-h>', lambda event: self.clear_history())
        self.bind('<Control-c>', lambda event: self._copy_result())

    def set_language(self, language: str):
        if language not in TRANSLATIONS:
            return
        self.current_language = language
        self.title(TRANSLATIONS[self.current_language]["title"])
        self.hint_label.configure(text=self._t("info"))
        self.status_label.configure(text=self._t("help"))
        self.history_title_label.configure(text="▣ " + self._t("history_title"))
        self.config(menu=self._build_menu())

    def _special_action(self, action: str):
        if action == "=":
            self.calculate()
        elif action == "Plot":
            self.plot_expression()
        elif action == "Import":
            self.import_history_json()
        elif action == "Export":
            self.export_history_json()
        elif action == "History":
            messagebox.showinfo(self._t("title"), self._t("help"))
        elif action == "Copy":
            self._copy_result()
        elif action == "d/dx":
            self.calculate_derivative()
        elif action == "∫":
            self.calculate_integral()
        elif action == "Conv":
            self.show_conversion_help()

    def _copy_result(self):
        result = self.expression.get()
        if result:
            self.clipboard_clear()
            self.clipboard_append(result)
            self.status_label.configure(text=self._t("copied"), fg=self.ACCENT_GREEN)
            self.after(2000, lambda: self.status_label.configure(text=self._t("help"), fg=self.FG_SECONDARY))
        else:
            self.status_label.configure(text=self._t("copy_empty"), fg=self.ACCENT_PINK)
            self.after(2000, lambda: self.status_label.configure(text=self._t("help"), fg=self.FG_SECONDARY))

    def on_button_press(self, value: str):
        current = self.expression.get()
        
        if value == "C":
            self.expression.set("")
            self.status_label.configure(text="⊘ " + self._t("empty_expression"), fg=self.ACCENT_GREEN)
            self.after(1500, lambda: self.status_label.configure(text=self._t("help"), fg=self.FG_SECONDARY))
            return

        if value == "DEL":
            pos = self.display.index("insert")
            if pos > 0:
                self.expression.set(current[:pos-1] + current[pos:])
                self.display.icursor(pos - 1)
            return

        pos = self.display.index("insert")
        
        if value == "Ans":
            if self.history_manager.records:
                result = str(self.history_manager.records[-1]["result"])
                self.expression.set(current[:pos] + result + current[pos:])
                self.display.icursor(pos + len(result))
            return

        if value in ("pi", "e"):
            self.expression.set(current[:pos] + value + current[pos:])
            self.display.icursor(pos + len(value))
            return

        if value == "i":
            self.expression.set(current[:pos] + "1j" + current[pos:])
            self.display.icursor(pos + 2)
            return

        if value == "sqrt":
            self.expression.set(current[:pos] + "sqrt(" + current[pos:])
            self.display.icursor(pos + 5)
            return

        if value == "log":
            self.expression.set(current[:pos] + "log(" + current[pos:])
            self.display.icursor(pos + 4)
            return

        if value == "ln":
            self.expression.set(current[:pos] + "ln(" + current[pos:])
            self.display.icursor(pos + 3)
            return

        if value == "fact":
            self.expression.set(current[:pos] + "factorial(" + current[pos:])
            self.display.icursor(pos + 10)
            return

        if value in ("sin", "cos", "tan", "abs", "exp", "root"):
            func_text = f"{value}("
            self.expression.set(current[:pos] + func_text + current[pos:])
            self.display.icursor(pos + len(func_text))
            return

        if value == "^":
            self.expression.set(current[:pos] + "**" + current[pos:])
            self.display.icursor(pos + 2)
            return

        self.expression.set(current[:pos] + value + current[pos:])
        self.display.icursor(pos + len(value))

    def _format_result(self, result):
        if isinstance(result, complex):
            real = format(result.real, ".10g")
            imag = format(abs(result.imag), ".10g")
            sign = "+" if result.imag >= 0 else "-"
            return f"({real}{sign}{imag}j)"
        if isinstance(result, float):
            return format(result, ".10g")
        return str(result)

    def calculate(self):
        expression = self.expression.get().strip()
        if not expression:
            self.status_label.configure(text=self._t("empty_expression"), fg=self.ACCENT_PINK)
            return

        try:
            result = evaluate(expression)
            display_result = self._format_result(result)
            record = self.history_manager.add(expression, display_result)
            self._add_history_entry(record)
            self.expression.set(display_result)
            self.display.icursor("end")
            self.status_label.configure(text=self._t("calculated"), fg=self.ACCENT_GREEN)
            self.after(2000, lambda: self.status_label.configure(text=self._t("help"), fg=self.FG_SECONDARY))
        except ValueError as error:
            self.status_label.configure(text="✗ " + str(error)[:50], fg=self.ACCENT_PINK)

    def _add_history_entry(self, record: dict):
        text = f"[{record['timestamp']}] {record['expression']} = {record['result']}"
        self.history_list.insert(0, text)
        if self.history_list.size() > 100:
            self.history_list.delete(100)

    def clear_history(self):
        self.history_manager.clear()
        self.history_list.delete(0, tk.END)
        self.status_label.configure(text=self._t("history_cleared"), fg=self.ACCENT_GREEN)
        self.after(2000, lambda: self.status_label.configure(text=self._t("help"), fg=self.FG_SECONDARY))

    def import_history_json(self):
        path = filedialog.askopenfilename(
            title=self._t("import_title"),
            filetypes=[("JSON files", "*.json"), ("All files", "*")],
        )
        if not path:
            return

        try:
            imported_records = self.history_manager.load_json_file(path)
        except Exception as error:
            self.status_label.configure(text="✗ " + str(error)[:40], fg=self.ACCENT_PINK)
            return

        choice = ImportTargetDialog(self, self._t("import_title"), TRANSLATIONS[self.current_language]).result
        if choice not in ("append", "replace"):
            return

        if choice == "replace":
            self.history_list.delete(0, tk.END)
            self.history_manager.clear()

        records = self.history_manager.import_records(imported_records, replace=(choice == "replace"))
        for record in records:
            self._add_history_entry(record)

        self.status_label.configure(text=self._t("imported", count=len(records)), fg=self.ACCENT_GREEN)
        self.after(2000, lambda: self.status_label.configure(text=self._t("help"), fg=self.FG_SECONDARY))

    def export_history_json(self):
        if not self.history_manager.records:
            messagebox.showwarning(self._t("title"), self._t("no_history"))
            return

        path = filedialog.asksaveasfilename(
            title=self._t("export_history"),
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*")],
        )
        if not path:
            return

        try:
            self.history_manager.save_json_file(path, self.history_manager.records)
            self.status_label.configure(text=self._t("exported"), fg=self.ACCENT_GREEN)
            self.after(2000, lambda: self.status_label.configure(text=self._t("help"), fg=self.FG_SECONDARY))
        except Exception as error:
            self.status_label.configure(text="✗ " + str(error)[:40], fg=self.ACCENT_PINK)

    def _on_history_double_click(self, event):
        selection = self.history_list.curselection()
        if not selection:
            return
        record = self.history_manager.records[self.history_list.size() - 1 - selection[0]]
        self.expression.set(record["expression"])
        self.display.icursor("end")
        self.status_label.configure(text="↳ " + self._t("help"), fg=self.ACCENT_CYAN)

    def plot_expression(self):
        expression = self.expression.get().strip()
        if "x" not in expression:
            self.status_label.configure(text=self._t("plot_no_x"), fg=self.ACCENT_PINK)
            return

        try:
            plot_window = tk.Toplevel(self)
            plot_window.title(self._t("plot_title"))
            plot_window.configure(bg=self.BG_PRIMARY)
            plot_window.geometry("700x500")
            
            width, height = 680, 460
            canvas = tk.Canvas(plot_window, width=width, height=height, bg=self.BG_PRIMARY, bd=2, relief="flat", highlightthickness=0)
            canvas.pack(padx=10, pady=10)

            x_min, x_max = -10.0, 10.0
            steps = 400
            points = []

            for index in range(steps + 1):
                x = x_min + (x_max - x_min) * index / steps
                value = evaluate(expression, {"x": x})
                if isinstance(value, complex):
                    points.append((x, value.real, value.imag))
                else:
                    points.append((x, float(value), 0.0))

            ys = [p[1] for p in points if isinstance(p[1], (int, float))]
            if not ys:
                raise ValueError(self._t("plot_error", error="No valid data"))

            y_min = min(ys)
            y_max = max(ys)
            if y_min == y_max:
                y_min -= 1
                y_max += 1

            x_scale = (width - 80) / (x_max - x_min)
            y_scale = (height - 80) / (y_max - y_min)
            x_offset, y_offset = 40, 40

            # Оси
            canvas.create_line(x_offset, height - y_offset, width - x_offset, height - y_offset, fill=self.FG_SECONDARY, width=2)
            canvas.create_line(x_offset, y_offset, x_offset, height - y_offset, fill=self.FG_SECONDARY, width=2)
            canvas.create_text(width - x_offset, height - y_offset + 16, text="x", anchor="nw", fill=self.ACCENT_CYAN, font=("SF Mono", 10))
            canvas.create_text(x_offset - 10, y_offset, text="y", anchor="nw", fill=self.ACCENT_CYAN, font=("SF Mono", 10))

            def transform(x, y):
                px = x_offset + (x - x_min) * x_scale
                py = height - y_offset - (y - y_min) * y_scale
                return px, py

            prev = None
            for x, y_real, _ in points:
                px, py = transform(x, y_real)
                if prev is not None:
                    canvas.create_line(prev[0], prev[1], px, py, fill=self.ACCENT_GREEN, width=2)
                prev = (px, py)

            canvas.create_text(10, 10, anchor="nw", text=expression, fill=self.ACCENT_PURPLE, font=("SF Mono", 11, "bold"))
            self.status_label.configure(text=self._t("plot_title"), fg=self.ACCENT_GREEN)
        except Exception as error:
            self.status_label.configure(text=self._t("plot_error", error=str(error)[:20]), fg=self.ACCENT_PINK)

    def calculate_derivative(self):
        expression = self.expression.get().strip()
        if not expression:
            self.status_label.configure(text=self._t("empty_expression"), fg=self.ACCENT_PINK)
            return

        x_value = simpledialog.askfloat(self._t("title"), self._t("derivative_prompt"))
        if x_value is None:
            return

        try:
            h = 1e-6
            y1 = evaluate(expression, {"x": x_value + h})
            y2 = evaluate(expression, {"x": x_value - h})
            derivative = (y1 - y2) / (2 * h)
            result_text = self._t("derivative_result", x=x_value, result=self._format_result(derivative))
            messagebox.showinfo(self._t("title"), result_text)
        except Exception as error:
            self.status_label.configure(text="✗ " + str(error)[:40], fg=self.ACCENT_PINK)

    def calculate_integral(self):
        expression = self.expression.get().strip()
        if not expression:
            self.status_label.configure(text=self._t("empty_expression"), fg=self.ACCENT_PINK)
            return

        bounds = simpledialog.askstring(self._t("title"), self._t("integral_prompt"))
        if not bounds:
            return

        try:
            start_str, end_str = [part.strip() for part in bounds.split(",")]
            start = float(start_str)
            end = float(end_str)
            if start == end:
                raise ValueError(self._t("invalid_range"))

            steps = 1000
            step = (end - start) / steps
            total = 0
            previous = evaluate(expression, {"x": start})
            for i in range(1, steps + 1):
                x = start + i * step
                current = evaluate(expression, {"x": x})
                total += (previous + current) * step / 2
                previous = current

            result_text = self._t("integral_result", start=start, end=end, result=self._format_result(total))
            messagebox.showinfo(self._t("title"), result_text)
        except Exception as error:
            self.status_label.configure(text="✗ " + str(error)[:40], fg=self.ACCENT_PINK)

    def show_conversion_help(self):
        messagebox.showinfo(self._t("title"), self._t("conversion_help"))