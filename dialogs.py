import tkinter as tk
from tkinter import simpledialog


class ImportTargetDialog(simpledialog.Dialog):
    def body(self, master):
        self.selected = tk.StringVar(value="append")
        tk.Label(master, text="Виберіть куди імпортувати дані історії:").grid(row=0, column=0, columnspan=2, pady=6)
        tk.Radiobutton(master, text="Додати до поточної історії", variable=self.selected, value="append").grid(row=1, column=0, sticky="w")
        tk.Radiobutton(master, text="Замінити поточну історію", variable=self.selected, value="replace").grid(row=2, column=0, sticky="w")
        return None

    def apply(self):
        self.result = self.selected.get()
