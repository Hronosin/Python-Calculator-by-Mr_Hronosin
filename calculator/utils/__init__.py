"""
📦 Utils Module
===============

Вспомогательные утилиты и компоненты:
- Пользовательские диалоги
- Валидация данных
- Вспомогательные функции

Модули:
    - dialogs.py: Кастомные диалоговые окна
"""

import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox


# =============================================================================
# ПОЛЬЗОВАТЕЛЬСКИЕ ДИАЛОГИ
# =============================================================================

class ImportTargetDialog(tk.Toplevel):
    """
    Диалог выбора действия при импорте истории
    
    Спрашивает у пользователя:
    - Заменить текущую историю
    - Добавить к существующей истории
    - Отмена
    """
    
    def __init__(self, parent, title: str = "Импорт", 
                 message: str = "Выберите действие:", 
                 texts: dict = None):
        """
        Инициализировать диалог
        
        Args:
            parent: Родительское окно
            title: Заголовок диалога
            message: Сообщение пользователю
            texts: Словарь переводов для кнопок
                   Ключи: "replace", "append", "cancel"
        """
        super().__init__(parent)
        self.title(title)
        self.result = None
        
        # Используем стандартные тексты если не переданы переводы
        if texts is None:
            texts = {
                "replace": "Заменить",
                "append": "Добавить",
                "cancel": "Отмена"
            }
        
        self.texts = texts
        
        # Центрируем окно
        self.geometry("300x150")
        self.resizable(False, False)
        
        # Создаём интерфейс
        self._create_ui(message)
        
        # Ждём ввода пользователя
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)
    
    def _create_ui(self, message: str):
        """
        Создать интерфейс диалога
        
        Args:
            message: Сообщение для отображения
        """
        # Сообщение
        msg_frame = tk.Frame(self)
        msg_frame.pack(pady=10)
        
        tk.Label(msg_frame, text=message, wraplength=280).pack()
        
        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text=self.texts["replace"], 
                 command=self._on_replace, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.texts["append"], 
                 command=self._on_append, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.texts["cancel"], 
                 command=self._on_cancel, width=10).pack(side=tk.LEFT, padx=5)
    
    def _on_replace(self):
        """Нажата кнопка Заменить"""
        self.result = "replace"
        self.destroy()
    
    def _on_append(self):
        """Нажата кнопка Добавить"""
        self.result = "append"
        self.destroy()
    
    def _on_cancel(self):
        """Нажата кнопка Отмена"""
        self.result = None
        self.destroy()


class FileDialog:
    """
    Вспомогательный класс для работы с файловыми диалогами
    
    Предоставляет удобные методы для выбора файлов
    """
    
    @staticmethod
    def save_file(title: str = "Сохранить файл", 
                 default_name: str = "history.json",
                 filetypes: tuple = None) -> str:
        """
        Диалог сохранения файла
        
        Args:
            title: Заголовок диалога
            default_name: Имя файла по умолчанию
            filetypes: Кортеж типов файлов ((название, расширение), ...)
        
        Returns:
            str: Путь к выбранному файлу или пусто если отменено
        """
        if filetypes is None:
            filetypes = (
                ("JSON файлы", "*.json"),
                ("Все файлы", "*.*")
            )
        
        return filedialog.asksaveasfilename(
            title=title,
            initialfile=default_name,
            filetypes=filetypes,
            defaultextension=".json"
        )
    
    @staticmethod
    def open_file(title: str = "Открыть файл",
                 filetypes: tuple = None) -> str:
        """
        Диалог открытия файла
        
        Args:
            title: Заголовок диалога
            filetypes: Кортеж типов файлов
        
        Returns:
            str: Путь к выбранному файлу или пусто если отменено
        """
        if filetypes is None:
            filetypes = (
                ("JSON файлы", "*.json"),
                ("Все файлы", "*.*")
            )
        
        return filedialog.askopenfilename(
            title=title,
            filetypes=filetypes
        )


# =============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =============================================================================

def show_info(title: str, message: str):
    """
    Показать информационное сообщение
    
    Args:
        title: Заголовок
        message: Текст сообщения
    """
    messagebox.showinfo(title, message)


def show_error(title: str, message: str):
    """
    Показать сообщение об ошибке
    
    Args:
        title: Заголовок
        message: Текст ошибки
    """
    messagebox.showerror(title, message)


def show_warning(title: str, message: str):
    """
    Показать предупреждение
    
    Args:
        title: Заголовок
        message: Текст предупреждения
    """
    messagebox.showwarning(title, message)


def ask_yes_no(title: str, message: str) -> bool:
    """
    Спросить пользователя Да/Нет
    
    Args:
        title: Заголовок
        message: Вопрос
    
    Returns:
        bool: True если Да, False если Нет
    """
    return messagebox.askyesno(title, message)
