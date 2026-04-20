import tkinter as tk
from tkinter import filedialog, messagebox

from calculator_core import evaluate
from dialogs import ImportTargetDialog
from history_manager import HistoryManager


class EngineeringCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Інженерний калькулятор")
        self.configure(bg="#f3f6fb")
        self.resizable(False, False)
        self.expression = tk.StringVar()
        self.history_manager = HistoryManager()
        self._build_ui()
        self._bind_keyboard()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)

        display_frame = tk.Frame(self, bg="#f3f6fb", padx=12, pady=12)
        display_frame.grid(row=0, column=0, sticky="nsew")

        self.display = tk.Entry(
            display_frame,
            textvariable=self.expression,
            font=("Segoe UI", 20, "bold"),
            bd=0,
            relief="flat",
            justify="right",
            width=28,
            highlightthickness=2,
            highlightbackground="#ced4da",
            highlightcolor="#4CAF50",
            insertbackground="#212529",
        )
        self.display.grid(row=0, column=0, columnspan=6, pady=(0, 12), ipady=12)
        self.display.focus()

        self.info_label = tk.Label(
            display_frame,
            text="Enter = обчислити · Esc = очистити · Ctrl+O = імпорт JSON · Ctrl+E = експорт JSON",
            font=("Segoe UI", 9),
            fg="#495057",
            bg="#f3f6fb",
            anchor="w",
        )
        self.info_label.grid(row=1, column=0, columnspan=6, sticky="w", pady=(0, 10))

        button_frame = tk.Frame(self, bg="#f3f6fb", padx=12, pady=6)
        button_frame.grid(row=1, column=0, sticky="nsew")

        button_map = [
            [("C", "#ff6b6b"), ("DEL", "#ffa94d"), ("(", "#adb5bd"), (")", "#adb5bd"), ("^", "#74c0fc")],
            [("7", "#ffffff"), ("8", "#ffffff"), ("9", "#ffffff"), ("/", "#74c0fc"), ("sqrt", "#74c0fc")],
            [("4", "#ffffff"), ("5", "#ffffff"), ("6", "#ffffff"), ("*", "#74c0fc"), ("log", "#74c0fc")],
            [("1", "#ffffff"), ("2", "#ffffff"), ("3", "#ffffff"), ("-", "#74c0fc"), ("ln", "#74c0fc")],
            [("0", "#ffffff"), (".", "#ffffff"), ("Ans", "#ffe066"), ("+", "#74c0fc"), ("=", "#38d9a9")],
            [("sin", "#74c0fc"), ("cos", "#74c0fc"), ("tan", "#74c0fc"), ("pi", "#74c0fc"), ("e", "#74c0fc")],
            [("fact", "#74c0fc"), ("Import", "#86efac"), ("Export", "#86efac"), ("History", "#86efac"), ("Clear", "#86efac"), ("Copy", "#86efac")],
        ]

        for row_index, row in enumerate(button_map, start=0):
            for col_index, button_data in enumerate(row):
                text, color = button_data
                width = 6 if text not in ("=", "Import", "Export") else 14
                button_command = self.on_button_press if text not in ("=", "Import", "Export", "History", "Clear", "Copy") else self._special_action
                button = tk.Button(
                    button_frame,
                    text=text,
                    bg=color,
                    fg="#212529",
                    activebackground="#ced4da",
                    activeforeground="#212529",
                    width=width,
                    height=2,
                    font=("Segoe UI", 11, "bold"),
                    relief="flat",
                    command=lambda t=text, fn=button_command: fn(t),
                )
                if text == "=":
                    button.configure(bg="#20c997", fg="#ffffff")
                button.grid(row=row_index, column=col_index, padx=4, pady=4, sticky="nsew")

        history_frame = tk.Frame(self, bg="#f3f6fb", padx=12, pady=12)
        history_frame.grid(row=0, column=1, rowspan=2, sticky="ns")
        tk.Label(history_frame, text="Історія обчислень", font=("Segoe UI", 12, "bold"), bg="#f3f6fb").pack(anchor="w", pady=(0, 8))

        self.history_list = tk.Listbox(history_frame, width=38, height=22, font=("Segoe UI", 10), bd=2, relief="sunken")
        self.history_list.pack(side="left", fill="y")
        self.history_list.bind("<Double-Button-1>", self._on_history_double_click)

        scrollbar = tk.Scrollbar(history_frame, orient="vertical", command=self.history_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_list.config(yscrollcommand=scrollbar.set)

        footer_frame = tk.Frame(self, bg="#f3f6fb", padx=12, pady=12)
        footer_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        tk.Label(
            footer_frame,
            text="Double-click record → повернути вираз · Ctrl+O = імпорт · Ctrl+H = очистити історію",
            font=("Segoe UI", 9),
            fg="#495057",
            bg="#f3f6fb",
        ).pack(anchor="w")

        self.columnconfigure(1, minsize=320)

        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Імпортувати історію JSON...", command=self.import_history_json)
        file_menu.add_command(label="Експортувати історію JSON...", command=self.export_history_json)
        file_menu.add_command(label="Очистити історію", command=self.clear_history)
        file_menu.add_separator()
        file_menu.add_command(label="Вийти", command=self.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        self.config(menu=menu_bar)

    def _bind_keyboard(self):
        self.bind('<Return>', lambda event: self.calculate())
        self.bind('<Escape>', lambda event: self.on_button_press('C'))
        self.bind('<BackSpace>', lambda event: self.on_button_press('DEL'))
        self.bind('<Delete>', lambda event: self.on_button_press('DEL'))
        self.bind('<Control-o>', lambda event: self.import_history_json())
        self.bind('<Control-e>', lambda event: self.export_history_json())
        self.bind('<Control-h>', lambda event: self.clear_history())
        self.bind('<Control-c>', lambda event: self._copy_result())

    def _special_action(self, action: str):
        if action == "=":
            self.calculate()
        elif action == "Import":
            self.import_history_json()
        elif action == "Export":
            self.export_history_json()
        elif action == "History":
            messagebox.showinfo("Історія", "Подвійний клік на записі вставляє вираз у поле вводу.")
        elif action == "Clear":
            self.clear_history()
        elif action == "Copy":
            self._copy_result()

    def _copy_result(self):
        result = self.expression.get()
        if result:
            self.clipboard_clear()
            self.clipboard_append(result)
            self.info_label.configure(text="Результат скопійовано в буфер обміну.")
        else:
            self.info_label.configure(text="Немає тексту для копіювання.")

    def on_button_press(self, value: str):
        current = self.expression.get()
        if value == "C":
            self.expression.set("")
            self.info_label.configure(text="Поле очищено.")
            return

        if value == "DEL":
            self.expression.set(current[:-1])
            return

        if value == "Ans":
            if self.history_manager.records:
                self.expression.set(current + str(self.history_manager.records[-1]["result"]))
            return

        if value == "pi":
            self.expression.set(current + "pi")
            return

        if value == "e":
            self.expression.set(current + "e")
            return

        if value == "sqrt":
            self.expression.set(current + "sqrt(")
            return

        if value == "log":
            self.expression.set(current + "log10(")
            return

        if value == "ln":
            self.expression.set(current + "log(")
            return

        if value == "fact":
            self.expression.set(current + "factorial(")
            return

        if value in ("sin", "cos", "tan"):
            self.expression.set(current + f"{value}(")
            return

        if value == "^":
            self.expression.set(current + "**")
            return

        self.expression.set(current + value)

    def calculate(self):
        expression = self.expression.get().strip()
        if not expression:
            self.info_label.configure(text="Введіть вираз для обчислення.")
            return

        try:
            result = evaluate(expression)
            display_result = round(result, 12) if isinstance(result, float) else result
            record = self.history_manager.add(expression, display_result)
            self._add_history_entry(record)
            self.expression.set(str(display_result))
            self.info_label.configure(text="Обчислено успішно. Натисніть Ctrl+C, щоб скопіювати результат.")
        except ValueError as error:
            messagebox.showerror("Помилка", f"Неможливо обчислити вираз:\n{error}")

    def _add_history_entry(self, record: dict):
        text = f"[{record['timestamp']}] {record['expression']} = {record['result']}"
        self.history_list.insert(tk.END, text)

    def clear_history(self):
        self.history_manager.clear()
        self.history_list.delete(0, tk.END)
        self.info_label.configure(text="Історія очищена.")

    def import_history_json(self):
        path = filedialog.askopenfilename(
            title="Виберіть JSON файл для імпорту історії",
            filetypes=[("JSON files", "*.json"), ("All files", "*")],
        )
        if not path:
            return

        try:
            imported_records = self.history_manager.load_json_file(path)
        except Exception as error:
            messagebox.showerror("Помилка", f"Не вдалося прочитати JSON файл:\n{error}")
            return

        choice = ImportTargetDialog(self).result
        if choice not in ("append", "replace"):
            return

        records = self.history_manager.import_records(imported_records, replace=(choice == "replace"))
        for record in records:
            self._add_history_entry(record)

        self.info_label.configure(text=f"Імпортовано {len(records)} записів історії.")

    def export_history_json(self):
        if not self.history_manager.records:
            messagebox.showwarning("Увага", "Немає записів історії для експорту.")
            return

        path = filedialog.asksaveasfilename(
            title="Зберегти історію як JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*")],
        )
        if not path:
            return

        try:
            self.history_manager.save_json_file(path, self.history_manager.records)
            self.info_label.configure(text=f"Історію експортовано до {path}.")
        except Exception as error:
            messagebox.showerror("Помилка", f"Не вдалося зберегти JSON файл:\n{error}")

    def _on_history_double_click(self, event):
        selection = self.history_list.curselection()
        if not selection:
            return
        record = self.history_manager.records[selection[0]]
        self.expression.set(record["expression"])
        self.info_label.configure(text="Вставлено вираз з історії.")
