import tkinter as tk
from tkinter import simpledialog


class ImportTargetDialog(simpledialog.Dialog):
    def __init__(self, parent, title, texts):
        self.texts = texts
        super().__init__(parent, title=title)

    def body(self, master):
        self.selected = tk.StringVar(value="append")
        tk.Label(master, text=self.texts["import_prompt"]).grid(row=0, column=0, columnspan=2, pady=6)
        tk.Radiobutton(master, text=self.texts["import_append"], variable=self.selected, value="append").grid(row=1, column=0, sticky="w")
        tk.Radiobutton(master, text=self.texts["import_replace"], variable=self.selected, value="replace").grid(row=2, column=0, sticky="w")
        return None

    def apply(self):
        self.result = self.selected.get()
