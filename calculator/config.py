"""
Configuration and localization for the engineering calculator.
"""

import os

# Language settings
LANGUAGE = os.getenv('CALC_LANG', 'ru')  # Default to Russian

# Localization dictionaries
LOCALES = {
    'ru': {
        'window_title': 'Инженерный калькулятор',
        'file_menu': 'Файл',
        'exit': 'Выход',
        'view_menu': 'Вид',
        'theme_menu': 'Тема',
        'dark_theme': 'Тёмная',
        'light_theme': 'Светлая',
        'lang_menu': 'Язык',
        'russian': 'Русский',
        'english': 'English',
        'restart_required': 'Требуется перезапуск для применения изменений',
        'history_title': 'История',
        'clear_history': 'очистить',
        'error': 'Ошибка',
        'memory': 'M',
        'degrees': 'DEG',
        'radians': 'RAD',
        'inverse': 'INV',
        'ans': 'ANS',
        'clear': 'AC',
        'delete': '⌫',
        'equals': '=',
        'plus': '+',
        'minus': '−',
        'multiply': '×',
        'divide': '÷',
        'modulo': 'mod',
        'power': 'xⁿ',
        'square': 'x²',
        'sqrt': '√',
        'cbrt': '∛',
        'log': 'log',
        'ln': 'ln',
        'log2': 'log₂',
        'exp': 'eˣ',
        'pow10': '10ˣ',
        'sin': 'sin',
        'cos': 'cos',
        'tan': 'tan',
        'sinh': 'sinh',
        'cosh': 'cosh',
        'tanh': 'tanh',
        'pi': 'π',
        'e_const': 'e',
        'phi': 'φ',
        'abs': '|x|',
        'fact': 'n!',
        'inv': '1/x',
        'pct': '%',
        'floor': '⌊x⌋',
        'ceil': '⌈x⌉',
        'round': 'rnd',
        'neg': '±',
        'dot': '.',
        'ee': 'EE',
        'mc': 'MC',
        'mr': 'MR',
        'mplus': 'M+',
        'mminus': 'M−',
        'deg_rad': 'DEG/RAD',
        'inv_toggle': 'INV',
        'pi_half': 'π/2',
        'units_title': 'Конвертер единиц',
        'from': 'Из:',
        'to': 'В:',
        'distance': 'Расстояние',
        'weight': 'Вес',
        'temperature': 'Температура',
        'time': 'Время',
        'volume': 'Объем',
        'area': 'Площадь',
        'speed': 'Скорость',
        'energy': 'Энергия',
        'pressure': 'Давление',
        'force': 'Сила',
    },
    'en': {
        'window_title': 'Engineering Calculator',
        'file_menu': 'File',
        'exit': 'Exit',
        'view_menu': 'View',
        'theme_menu': 'Theme',
        'dark_theme': 'Dark',
        'light_theme': 'Light',
        'lang_menu': 'Language',
        'russian': 'Русский',
        'english': 'English',
        'restart_required': 'Restart required to apply changes',
        'history_title': 'History',
        'clear_history': 'clear',
        'error': 'Error',
        'memory': 'M',
        'degrees': 'DEG',
        'radians': 'RAD',
        'inverse': 'INV',
        'ans': 'ANS',
        'clear': 'AC',
        'delete': '⌫',
        'equals': '=',
        'plus': '+',
        'minus': '-',
        'multiply': '*',
        'divide': '/',
        'modulo': 'mod',
        'power': 'x^y',
        'square': 'x²',
        'sqrt': '√',
        'cbrt': '∛',
        'log': 'log',
        'ln': 'ln',
        'log2': 'log₂',
        'exp': 'e^x',
        'pow10': '10^x',
        'sin': 'sin',
        'cos': 'cos',
        'tan': 'tan',
        'sinh': 'sinh',
        'cosh': 'cosh',
        'tanh': 'tanh',
        'pi': 'π',
        'e_const': 'e',
        'phi': 'φ',
        'abs': '|x|',
        'fact': 'n!',
        'inv': '1/x',
        'pct': '%',
        'floor': '⌊x⌋',
        'ceil': '⌈x⌉',
        'round': 'rnd',
        'neg': '±',
        'dot': '.',
        'ee': 'EE',
        'mc': 'MC',
        'mr': 'MR',
        'mplus': 'M+',
        'mminus': 'M-',
        'deg_rad': 'DEG/RAD',
        'inv_toggle': 'INV',
        'pi_half': 'π/2',
        'units_title': 'Units Converter',
        'from': 'From:',
        'to': 'To:',
        'distance': 'Distance',
        'weight': 'Weight',
        'temperature': 'Temperature',
        'time': 'Time',
        'volume': 'Volume',
        'area': 'Area',
        'speed': 'Speed',
        'energy': 'Energy',
        'pressure': 'Pressure',
        'force': 'Force',
    }
}
}

def get_text(key):
    """Get localized text for the current language."""
    return LOCALES.get(LANGUAGE, LOCALES['ru']).get(key, key)

# History file
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'history.json')

# State file
STATE_FILE = os.path.join(os.path.dirname(__file__), 'state.json')

# Theme file
THEME_FILE = os.path.join(os.path.dirname(__file__), 'theme.txt')

# Language file
LANG_FILE = os.path.join(os.path.dirname(__file__), 'lang.txt')

# Themes
THEMES = {
    'dark': {
        'DARK_BG': '#1a1a1f',
        'PANEL_BG': '#22222a',
        'CARD_BG': '#2b2b36',
        'CARD_HOVER': '#333340',
        'DISPLAY_BG': '#14141a',
        'TEXT_WHITE': '#eaeaf0',
        'TEXT_MUTED': '#8888a0',
        'TEXT_EXPR': '#5555aa',
        'ACCENT_BLUE': '#4a7cff',
        'ACCENT_GREEN': '#30d988',
        'ACCENT_AMBER': '#f5a623',
        'ACCENT_RED': '#ff5a5a',
        'BORDER': '#3a3a4a',
    },
    'light': {
        'DARK_BG': '#f5f5f5',
        'PANEL_BG': '#ffffff',
        'CARD_BG': '#e0e0e0',
        'CARD_HOVER': '#d0d0d0',
        'DISPLAY_BG': '#ffffff',
        'TEXT_WHITE': '#000000',
        'TEXT_MUTED': '#666666',
        'TEXT_EXPR': '#333333',
        'ACCENT_BLUE': '#0066cc',
        'ACCENT_GREEN': '#009900',
        'ACCENT_AMBER': '#ff9900',
        'ACCENT_RED': '#cc0000',
        'BORDER': '#cccccc',
    }
}

CURRENT_THEME = 'dark'

def load_theme():
    global CURRENT_THEME
    if os.path.exists(THEME_FILE):
        try:
            with open(THEME_FILE, 'r') as f:
                CURRENT_THEME = f.read().strip()
        except:
            pass

def save_theme(theme):
    global CURRENT_THEME
    CURRENT_THEME = theme
    try:
        with open(THEME_FILE, 'w') as f:
            f.write(theme)
    except:
        pass

def load_language():
    global LANGUAGE
    if os.path.exists(LANG_FILE):
        try:
            with open(LANG_FILE, 'r') as f:
                LANGUAGE = f.read().strip()
        except:
            pass

def save_language(lang):
    global LANGUAGE
    LANGUAGE = lang
    try:
        with open(LANG_FILE, 'w') as f:
            f.write(lang)
    except:
        pass

# Load settings on import
load_theme()
load_language()