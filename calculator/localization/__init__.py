"""
📦 Localization Module
======================

Система поддержки многоязычного интерфейса с кешированием.

Поддерживаемые языки (8):
    - uk - Українська (Ukrainian)
    - en - English
    - ru - Русский (Russian)
    - de - Deutsch (German)
    - fr - Français (French)
    - es - Español (Spanish)
    - pl - Polski (Polish)
    - ja - 日本語 (Japanese)

Использование:
    from calculator.localization import Localizator
    
    loc = Localizator("uk")  # Украинский
    text = loc.get("hello")
"""


# =============================================================================
# СЛОВАРИ ПЕРЕВОДОВ (8 ЯЗЫКОВ)
# =============================================================================

TRANSLATIONS = {
    # Украинский
    "uk": {
        # Кнопки
        "equals": "=", "clear": "C", "delete": "DEL",
        "add": "+", "subtract": "−", "multiply": "×", "divide": "÷",
        
        # Функции
        "sin": "sin", "cos": "cos", "tan": "tan",
        "asin": "asin", "acos": "acos", "atan": "atan",
        "sinh": "sinh", "cosh": "cosh", "tanh": "tanh",
        "sqrt": "√", "ln": "ln", "log": "log", "log10": "lg",
        "exp": "e^x", "factorial": "n!", "power": "x^y", "root": "root",
        
        # Операции
        "plot": "Графік", "derivative": "Похідна", "integral": "Інтеграл",
        "history": "Історія", "convert": "Конвертер",
        
        # Меню
        "file": "Файл", "edit": "Редагування", "tools": "Інструменти",
        "language": "Мова", "view": "Вид", "help": "Допомога",
        
        # Операції файла
        "import": "Імпортувати", "export": "Експортувати",
        "clear_history": "Очистити історію", "exit": "Вихід",
        
        # Сообщения
        "error": "Помилка", "success": "Успіх",
        "input_error": "Помилка введення", "calculation_error": "Помилка обчислення",
        "zero_division": "Ділення на нуль", "invalid_expression": "Невірний вираз",
        
        # Диалоги
        "import_question": "Заміни існуючу історію чи додай?",
        "replace": "Замінити", "append": "Додати", "cancel": "Скасувати",
        
        # Статус бар
        "ready": "Готово", "calculating": "Обчислення...",
    },
    
    # English
    "en": {
        "equals": "=", "clear": "C", "delete": "DEL",
        "add": "+", "subtract": "−", "multiply": "×", "divide": "÷",
        
        "sin": "sin", "cos": "cos", "tan": "tan",
        "asin": "asin", "acos": "acos", "atan": "atan",
        "sinh": "sinh", "cosh": "cosh", "tanh": "tanh",
        "sqrt": "√", "ln": "ln", "log": "log", "log10": "lg",
        "exp": "e^x", "factorial": "n!", "power": "x^y", "root": "root",
        
        "plot": "Graph", "derivative": "Derivative", "integral": "Integral",
        "history": "History", "convert": "Convert",
        
        "file": "File", "edit": "Edit", "tools": "Tools",
        "language": "Language", "view": "View", "help": "Help",
        
        "import": "Import", "export": "Export",
        "clear_history": "Clear History", "exit": "Exit",
        
        "error": "Error", "success": "Success",
        "input_error": "Input Error", "calculation_error": "Calculation Error",
        "zero_division": "Division by Zero", "invalid_expression": "Invalid Expression",
        
        "import_question": "Replace history or append?",
        "replace": "Replace", "append": "Append", "cancel": "Cancel",
        
        "ready": "Ready", "calculating": "Calculating...",
    },
    
    # Русский
    "ru": {
        "equals": "=", "clear": "C", "delete": "DEL",
        "add": "+", "subtract": "−", "multiply": "×", "divide": "÷",
        
        "sin": "sin", "cos": "cos", "tan": "tan",
        "asin": "asin", "acos": "acos", "atan": "atan",
        "sinh": "sinh", "cosh": "cosh", "tanh": "tanh",
        "sqrt": "√", "ln": "ln", "log": "log", "log10": "lg",
        "exp": "e^x", "factorial": "n!", "power": "x^y", "root": "root",
        
        "plot": "График", "derivative": "Производная", "integral": "Интеграл",
        "history": "История", "convert": "Конвертер",
        
        "file": "Файл", "edit": "Редактирование", "tools": "Инструменты",
        "language": "Язык", "view": "Вид", "help": "Справка",
        
        "import": "Импортировать", "export": "Экспортировать",
        "clear_history": "Очистить историю", "exit": "Выход",
        
        "error": "Ошибка", "success": "Успех",
        "input_error": "Ошибка ввода", "calculation_error": "Ошибка расчёта",
        "zero_division": "Деление на ноль", "invalid_expression": "Неверное выражение",
        
        "import_question": "Заменить историю или добавить?",
        "replace": "Заменить", "append": "Добавить", "cancel": "Отмена",
        
        "ready": "Готово", "calculating": "Вычисление...",
    },
    
    # Deutsch (German)
    "de": {
        "equals": "=", "clear": "C", "delete": "DEL",
        "add": "+", "subtract": "−", "multiply": "×", "divide": "÷",
        
        "sin": "sin", "cos": "cos", "tan": "tan",
        "asin": "asin", "acos": "acos", "atan": "atan",
        "sinh": "sinh", "cosh": "cosh", "tanh": "tanh",
        "sqrt": "√", "ln": "ln", "log": "log", "log10": "lg",
        "exp": "e^x", "factorial": "n!", "power": "x^y", "root": "root",
        
        "plot": "Graphik", "derivative": "Ableitung", "integral": "Integral",
        "history": "Verlauf", "convert": "Konvertieren",
        
        "file": "Datei", "edit": "Bearbeiten", "tools": "Werkzeuge",
        "language": "Sprache", "view": "Ansicht", "help": "Hilfe",
        
        "import": "Importieren", "export": "Exportieren",
        "clear_history": "Verlauf löschen", "exit": "Beenden",
        
        "error": "Fehler", "success": "Erfolg",
        "input_error": "Eingabefehler", "calculation_error": "Rechenfehler",
        "zero_division": "Division durch Null", "invalid_expression": "Ungültiger Ausdruck",
        
        "import_question": "Verlauf ersetzen oder hinzufügen?",
        "replace": "Ersetzen", "append": "Hinzufügen", "cancel": "Abbrechen",
        
        "ready": "Bereit", "calculating": "Berechnung läuft...",
    },
    
    # Français (French)
    "fr": {
        "equals": "=", "clear": "C", "delete": "DEL",
        "add": "+", "subtract": "−", "multiply": "×", "divide": "÷",
        
        "sin": "sin", "cos": "cos", "tan": "tan",
        "asin": "asin", "acos": "acos", "atan": "atan",
        "sinh": "sinh", "cosh": "cosh", "tanh": "tanh",
        "sqrt": "√", "ln": "ln", "log": "log", "log10": "lg",
        "exp": "e^x", "factorial": "n!", "power": "x^y", "root": "root",
        
        "plot": "Graphique", "derivative": "Dérivée", "integral": "Intégrale",
        "history": "Historique", "convert": "Convertir",
        
        "file": "Fichier", "edit": "Édition", "tools": "Outils",
        "language": "Langue", "view": "Affichage", "help": "Aide",
        
        "import": "Importer", "export": "Exporter",
        "clear_history": "Effacer l'historique", "exit": "Quitter",
        
        "error": "Erreur", "success": "Succès",
        "input_error": "Erreur d'entrée", "calculation_error": "Erreur de calcul",
        "zero_division": "Division par zéro", "invalid_expression": "Expression invalide",
        
        "import_question": "Remplacer l'historique ou ajouter?",
        "replace": "Remplacer", "append": "Ajouter", "cancel": "Annuler",
        
        "ready": "Prêt", "calculating": "Calcul en cours...",
    },
    
    # Español (Spanish)
    "es": {
        "equals": "=", "clear": "C", "delete": "DEL",
        "add": "+", "subtract": "−", "multiply": "×", "divide": "÷",
        
        "sin": "sin", "cos": "cos", "tan": "tan",
        "asin": "asin", "acos": "acos", "atan": "atan",
        "sinh": "sinh", "cosh": "cosh", "tanh": "tanh",
        "sqrt": "√", "ln": "ln", "log": "log", "log10": "lg",
        "exp": "e^x", "factorial": "n!", "power": "x^y", "root": "root",
        
        "plot": "Gráfico", "derivative": "Derivada", "integral": "Integral",
        "history": "Historial", "convert": "Convertir",
        
        "file": "Archivo", "edit": "Editar", "tools": "Herramientas",
        "language": "Idioma", "view": "Ver", "help": "Ayuda",
        
        "import": "Importar", "export": "Exportar",
        "clear_history": "Borrar historial", "exit": "Salir",
        
        "error": "Error", "success": "Éxito",
        "input_error": "Error de entrada", "calculation_error": "Error de cálculo",
        "zero_division": "División por cero", "invalid_expression": "Expresión inválida",
        
        "import_question": "¿Reemplazar historial o añadir?",
        "replace": "Reemplazar", "append": "Añadir", "cancel": "Cancelar",
        
        "ready": "Listo", "calculating": "Calculando...",
    },
    
    # Polski (Polish)
    "pl": {
        "equals": "=", "clear": "C", "delete": "DEL",
        "add": "+", "subtract": "−", "multiply": "×", "divide": "÷",
        
        "sin": "sin", "cos": "cos", "tan": "tan",
        "asin": "asin", "acos": "acos", "atan": "atan",
        "sinh": "sinh", "cosh": "cosh", "tanh": "tanh",
        "sqrt": "√", "ln": "ln", "log": "log", "log10": "lg",
        "exp": "e^x", "factorial": "n!", "power": "x^y", "root": "root",
        
        "plot": "Wykres", "derivative": "Pochodna", "integral": "Całka",
        "history": "Historia", "convert": "Konwertuj",
        
        "file": "Plik", "edit": "Edycja", "tools": "Narzędzia",
        "language": "Język", "view": "Widok", "help": "Pomoc",
        
        "import": "Importuj", "export": "Eksportuj",
        "clear_history": "Wyczyść historię", "exit": "Wyjście",
        
        "error": "Błąd", "success": "Powodzenie",
        "input_error": "Błąd wejścia", "calculation_error": "Błąd obliczenia",
        "zero_division": "Dzielenie przez zero", "invalid_expression": "Nieprawidłowe wyrażenie",
        
        "import_question": "Zastąpić historię czy dołączyć?",
        "replace": "Zastąpić", "append": "Dołączyć", "cancel": "Anuluj",
        
        "ready": "Gotowe", "calculating": "Obliczanie...",
    },
    
    # 日本語 (Japanese)
    "ja": {
        "equals": "=", "clear": "C", "delete": "DEL",
        "add": "+", "subtract": "−", "multiply": "×", "divide": "÷",
        
        "sin": "sin", "cos": "cos", "tan": "tan",
        "asin": "asin", "acos": "acos", "atan": "atan",
        "sinh": "sinh", "cosh": "cosh", "tanh": "tanh",
        "sqrt": "√", "ln": "ln", "log": "log", "log10": "lg",
        "exp": "e^x", "factorial": "n!", "power": "x^y", "root": "root",
        
        "plot": "グラフ", "derivative": "微分", "integral": "積分",
        "history": "履歴", "convert": "変換",
        
        "file": "ファイル", "edit": "編集", "tools": "ツール",
        "language": "言語", "view": "表示", "help": "ヘルプ",
        
        "import": "インポート", "export": "エクスポート",
        "clear_history": "履歴をクリア", "exit": "終了",
        
        "error": "エラー", "success": "成功",
        "input_error": "入力エラー", "calculation_error": "計算エラー",
        "zero_division": "ゼロで除算", "invalid_expression": "無効な式",
        
        "import_question": "履歴を置き換えるか追加しますか?",
        "replace": "置き換え", "append": "追加", "cancel": "キャンセル",
        
        "ready": "準備完了", "calculating": "計算中...",
    },
}


# =============================================================================
# КЛАСС ЛОКАЛИЗАТОРА (С КЕШИРОВАНИЕМ И ОПТИМИЗАЦИЕЙ)
# =============================================================================

class Localizator:
    """
    Система управления переводами и локализацией интерфейса
    
    Особенности:
    - Поддержка 8 языков с кешированием
    - Форматирование строк с параметрами
    - Быстрые запросы через кеш
    - Безопасная обработка ошибок
    
    Поддерживаемые языки:
        uk - Українська       en - English        ru - Русский
        de - Deutsch          fr - Français       es - Español
        pl - Polski          ja - 日本語
    
    Example:
        >>> loc = Localizator("uk")
        >>> loc.get("ready")
        "Готово"
        
        >>> loc.set_language("en")
        >>> loc.get("ready")
        "Ready"
    """
    
    # Поддерживаемые языки (8)
    SUPPORTED_LANGUAGES = {"uk", "en", "ru", "de", "fr", "es", "pl", "ja"}
    
    # Язык по умолчанию
    DEFAULT_LANGUAGE = "uk"
    
    # Кеш переводов (оптимизация производительности)
    _cache = {}
    
    def __init__(self, language: str = "uk"):
        """
        Инициализировать локализатор
        
        Args:
            language: Код языка (uk/en/ru/de/fr/es/pl/ja)
                     По умолчанию украинский ("uk")
        
        Raises:
            ValueError: Если язык не поддерживается
        """
        self.set_language(language)
    
    def set_language(self, language: str) -> None:
        """
        Установить текущий язык
        
        Args:
            language: Код языка (uk/en/ru/de/fr/es/pl/ja)
        
        Raises:
            ValueError: Если язык не поддерживается
        
        Example:
            >>> loc = Localizator()
            >>> loc.set_language("de")  # Переключиться на немецкий
        """
        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Язык '{language}' не поддерживается. "
                f"Доступны: {', '.join(sorted(self.SUPPORTED_LANGUAGES))}"
            )
        self.current_language = language
        
        # Инициализируем кеш для этого языка если ещё нет
        if language not in self._cache:
            self._cache[language] = TRANSLATIONS.get(language, {})
    
    def get(self, key: str, **kwargs) -> str:
        """
        Получить переведённую строку с кешированием
        
        Если передан **kwargs, форматирует строку с параметрами.
        
        Args:
            key: Ключ строки для поиска
            **kwargs: Параметры для форматирования ({name} → value)
        
        Returns:
            str: Переведённая строка или исходный ключ если не найдена
        
        Example:
            >>> loc = Localizator("uk")
            >>> loc.get("ready")
            "Готово"
            
            >>> loc.get("error")  # Из ru при текущем en возвращает ключ
            "error"
        """
        # Получаем кешированный словарь переводов текущего языка
        translations = self._cache.get(self.current_language, {})
        
        # Получаем перевод (если не найден - возвращаем ключ)
        text = translations.get(key, key)
        
        # Форматируем строку если переданы параметры (оптимизировано)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                # Если параметр не найден в строке, возвращаем как есть
                pass
        
        return text
    
    def get_all_translations(self, key: str) -> dict:
        """
        Получить переводы ключа на все доступные языки
        
        Полезно для отладки и проверки полноты локализации.
        
        Args:
            key: Ключ строки для поиска
        
        Returns:
            dict: Словарь {язык: перевод}
        
        Example:
            >>> loc = Localizator()
            >>> loc.get_all_translations("ready")
            {'uk': 'Готово', 'en': 'Ready', 'ru': 'Готово', ...}
        """
        result = {}
        for lang in self.SUPPORTED_LANGUAGES:
            translations = self._cache.get(lang, TRANSLATIONS.get(lang, {}))
            result[lang] = translations.get(key, key)
        return result
    
    def get_supported_languages(self) -> list:
        """
        Получить список всех поддерживаемых языков
        
        Returns:
            list: Отсортированный список кодов языков
        
        Example:
            >>> loc = Localizator()
            >>> loc.get_supported_languages()
            ['de', 'en', 'es', 'fr', 'ja', 'pl', 'ru', 'uk']
        """
        return sorted(self.SUPPORTED_LANGUAGES)
    
    @staticmethod
    def get_language_name(lang_code: str) -> str:
        """
        Получить полное название языка
        
        Args:
            lang_code: Код языка (uk/en/ru/de/fr/es/pl/ja)
        
        Returns:
            str: Полное название на английском
        
        Example:
            >>> Localizator.get_language_name("uk")
            "Ukrainian"
        """
        names = {
            "uk": "Ukrainian",
            "en": "English",
            "ru": "Russian",
            "de": "German",
            "fr": "French",
            "es": "Spanish",
            "pl": "Polish",
            "ja": "Japanese",
        }
        return names.get(lang_code, lang_code)
    
    def get_language_list(self) -> list:
        """
        Получить список доступных языков
        
        Returns:
            list: Коды доступных языков
        """
        return list(self.SUPPORTED_LANGUAGES)
    
    def get_all_translations(self, key: str) -> dict:
        """
        Получить переводы ключа на все языки
        
        Args:
            key: Ключ для поиска
        
        Returns:
            dict: Словарь переводов {код_языка: текст}
        
        Example:
            >>> loc = Localizator()
            >>> loc.get_all_translations("hello")
            {'uk': 'Привіт', 'en': 'Hello', 'ru': 'Привет'}
        """
        result = {}
        for lang in self.SUPPORTED_LANGUAGES:
            result[lang] = TRANSLATIONS[lang].get(key, key)
        return result
