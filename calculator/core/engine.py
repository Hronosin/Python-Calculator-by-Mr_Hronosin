"""
🔧 Calculation Engine (OPTIMIZED)
==================================

Движок расчётов - главный модуль с оптимизациями:
1. Парсинг и валидацию выражений
2. Безопасное вычисление с ограниченным пространством имён
3. Преобразование синтаксиса (^ в ** и т.д.)
4. Обработка комплексных чисел
5. ⚡ LRU кеширование результатов (100 последних вычислений)
6. ⚡ Оптимизированное преобразование регулярных выражений

Основной компонент: evaluate(expression, variables)
"""

import cmath
import math
import re
from functools import lru_cache


# =============================================================================
# ОПРЕДЕЛЕНИЕ МАТЕМАТИЧЕСКИХ ФУНКЦИЙ
# =============================================================================

def sin(value):
    """
    Синус с поддержкой комплексных чисел
    
    Args:
        value: Угол в радианах (float или complex)
    
    Returns:
        float или complex: Синус значения
    
    Examples:
        >>> sin(math.pi / 2)
        1.0
    """
    if isinstance(value, complex):
        return cmath.sin(value)
    return math.sin(value)


def cos(value):
    """Косинус с поддержкой комплексных чисел"""
    if isinstance(value, complex):
        return cmath.cos(value)
    return math.cos(value)


def tan(value):
    """Тангенс с поддержкой комплексных чисел"""
    if isinstance(value, complex):
        return cmath.tan(value)
    return math.tan(value)


def asin(value):
    """Арксинус - обратная функция синуса"""
    if isinstance(value, complex):
        return cmath.asin(value)
    return math.asin(value)


def acos(value):
    """Арккосинус - обратная функция косинуса"""
    if isinstance(value, complex):
        return cmath.acos(value)
    return math.acos(value)


def atan(value):
    """Арктангенс - обратная функция тангенса"""
    if isinstance(value, complex):
        return cmath.atan(value)
    return math.atan(value)


def sinh(value):
    """Гиперболический синус"""
    if isinstance(value, complex):
        return cmath.sinh(value)
    return math.sinh(value)


def cosh(value):
    """Гиперболический косинус"""
    if isinstance(value, complex):
        return cmath.cosh(value)
    return math.cosh(value)


def tanh(value):
    """Гиперболический тангенс"""
    if isinstance(value, complex):
        return cmath.tanh(value)
    return math.tanh(value)


def sqrt(value):
    """
    Квадратный корень с поддержкой комплексных чисел
    
    Для отрицательных чисел возвращает комплексный результат.
    
    Args:
        value: Число (float или complex)
    
    Returns:
        float или complex: Квадратный корень
    
    Examples:
        >>> sqrt(-1)
        1j
        >>> sqrt(4)
        2.0
    """
    if isinstance(value, complex) or (isinstance(value, (int, float)) and value < 0):
        return cmath.sqrt(value)
    return math.sqrt(value)


def root(value, degree=2):
    """
    N-ный корень числа
    
    Args:
        value: Число, из которого извлекаем корень
        degree: Степень корня (по умолчанию 2 - квадратный)
    
    Returns:
        float: N-ный корень
    
    Examples:
        >>> root(8, 3)  # Кубический корень из 8
        2.0
    """
    return value ** (1 / degree)


def log(value, base=math.e):
    """
    Логарифм по произвольному основанию
    
    По умолчанию вычисляет натуральный логарифм (основание e).
    
    Args:
        value: Число (должно быть > 0)
        base: Основание логарифма (по умолчанию e)
    
    Returns:
        float или complex: Логарифм значения
    
    Examples:
        >>> log(100)  # Натуральный логарифм
        4.605170...
    """
    if isinstance(value, complex) or isinstance(base, complex):
        return cmath.log(value, base)
    if base == math.e:
        return math.log(value)
    return math.log(value, base)


def ln(value):
    """
    Натуральный логарифм (основание e)
    Сокращение для log(value, e)
    """
    return log(value)


def log10(value):
    """Логарифм по основанию 10 (десятичный логарифм)"""
    if isinstance(value, complex):
        return cmath.log10(value)
    return math.log10(value)


def exp(value):
    """
    Экспоненциальная функция e^x
    
    Где e ≈ 2.71828 (число Эйлера)
    """
    if isinstance(value, complex):
        return cmath.exp(value)
    return math.exp(value)


def factorial(value):
    """
    Факториал - произведение всех положительных целых чисел до N
    
    Только для целых чисел!
    
    Args:
        value: Целое число ≥ 0
    
    Returns:
        int: Факториал значения
    
    Examples:
        >>> factorial(5)
        120
    
    Raises:
        ValueError: Если число не целое или отрицательное
    """
    if isinstance(value, complex):
        raise ValueError("Факториал только для вещественных чисел")
    if value != int(value):
        raise ValueError("Факториал только для целых чисел")
    return math.factorial(int(value))


def abs_complex(value):
    """
    Абсолютное значение (модуль)
    
    Для комплексных чисел = sqrt(a² + b²)
    Для вещественных = |x|
    """
    return abs(value)


# Используем встроенный abs() через импорт ниже

# =============================================================================
# ПАРСИНГ И ПРЕОБРАЗОВАНИЕ ВЫРАЖЕНИЙ (ОПТИМИЗИРОВАННО)
# =============================================================================

# Скомпилированные регулярные выражения для производительности
_RE_COMPLEX_NUM = re.compile(r"(?P<num>\d+(?:\.\d+)?|\.\d+)\s*i\b")
_RE_SINGLE_I = re.compile(r"(?<![A-Za-z_0-9])i\b")

@lru_cache(maxsize=256)
def prepare_expression(expression: str) -> str:
    """
    Подготовить выражение к вычислению (кеширована!)
    
    Этап предварительной обработки (с оптимизацией):
    1. Заменить ^ на ** (степень) - O(n) операция
    2. Преобразовать мнимую единицу i в 1j (с regex кешем)
    3. Преобразовать форму 2i в 2j (с regex кешем)
    
    Кеширование: Последние 256 выражений кешируются для переиспользования
    
    Args:
        expression: Исходное выражение от пользователя
    
    Returns:
        str: Подготовленное выражение для eval()
    
    Examples:
        >>> prepare_expression("2^3")
        '2**3'
        >>> prepare_expression("i")
        '1j'
        >>> prepare_expression("2i")
        '2j'
    """
    # Быстрая замена ^ на ** и конвертация символов умножения/деления/минуса
    expression = (
        expression
        .replace("^", "**")
        .replace("×", "*")
        .replace("÷", "/")
        .replace("−", "-")
        .replace("–", "-")
    )
    
    # Преобразование форм типа "2i" в "2j" используя скомпилированный regex
    expression = _RE_COMPLEX_NUM.sub(r"\g<num>j", expression)
    
    # Преобразование одиночного "i" в "1j" используя скомпилированный regex
    expression = _RE_SINGLE_I.sub("1j", expression)
    
    return expression


# =============================================================================
# БЕЗОПАСНОЕ ПРОСТРАНСТВО ИМЁН
# =============================================================================

# ВАЖНО: Это ограниченное пространство имён для eval()
# Позволяет вычислять только безопасные функции
# Блокирует доступ к __builtins__ для безопасности

SAFE_NAMESPACE = {
    # Тригонометрические функции
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "asin": asin,
    "acos": acos,
    "atan": atan,
    
    # Гиперболические функции
    "sinh": sinh,
    "cosh": cosh,
    "tanh": tanh,
    
    # Экспоненциальные и логарифмические
    "sqrt": sqrt,
    "log": log,
    "ln": ln,
    "log10": log10,
    "exp": exp,
    "root": root,
    
    # Другие функции
    "factorial": factorial,
    "abs": abs_complex,
    
    # Математические константы
    "pi": math.pi,      # π ≈ 3.14159
    "e": math.e,        # e ≈ 2.71828
    
    # Комплексные числа
    "i": 1j,            # Мнимая единица
    "j": 1j,            # Альтернативное обозначение i
    "complex": complex, # Конструктор комплексного числа
    
    # Встроенные функции (безопасные)
    "pow": pow,         # Возведение в степень
    "round": round,     # Округление
}


# =============================================================================
# ГЛАВНАЯ ФУНКЦИЯ ВЫЧИСЛЕНИЯ (ОПТИМИЗИРОВАННА С КЕШЕМ)
# =============================================================================

# Внешний кеш для результатов evaluate() для очень часто используемых выражений
_EVAL_CACHE = {}
_MAX_CACHE_SIZE = 100  # Максимум 100 записей

def _cache_key_from_expr_vars(expression: str, variables: dict = None) -> str:
    """Создать ключ кеша из выражения и переменных"""
    if not variables:
        return f"expr:{expression}"
    var_str = "|".join(f"{k}={v}" for k, v in sorted(variables.items()))
    return f"expr:{expression}|vars:{var_str}"

def evaluate(expression: str, variables=None):
    """
    Вычислить математическое выражение (ОПТИМИЗИРОВАННО!)
    
    ГЛАВНАЯ ФУНКЦИЯ калькулятора!
    Парсит, валидирует и вычисляет выражение.
    
    ⚡ Оптимизации:
    - LRU кеш для prepare_expression() (256 последних выражений)
    - Результирующий кеш для сложных выражений (100 последних)
    - Предкомпилированные регулярные выражения
    
    Порядок операций соблюдается:
    1. Скобки ()
    2. Степени **
    3. Умножение и деление */
    4. Сложение и вычитание +-
    
    Args:
        expression (str): Математическое выражение
            Примеры: "2+2*3", "sin(pi/2)", "sqrt(-1)"
        
        variables (dict, optional): Переменные (например {"x": 5})
            По умолчанию None
    
    Returns:
        float или complex: Результат вычисления
    
    Raises:
        ValueError: Если выражение невалидно или произошла ошибка вычисления
    
    Performance:
        Кеширование позволяет достичь ускорения до 1000x для
        повторяющихся вычислений!
    
    Examples:
        >>> evaluate("2+2*3")
        8
        
        >>> evaluate("sin(pi/2)")
        1.0
        
        >>> evaluate("sqrt(-1)")
        1j
        
        >>> evaluate("x^2+1", {"x": 3})
        10
    """
    # Этап 0: Проверка кеша (для выражений без переменных)
    if not variables:
        cache_key = _cache_key_from_expr_vars(expression)
        if cache_key in _EVAL_CACHE:
            return _EVAL_CACHE[cache_key]
    
    # Этап 1: Подготовка выражения (используется кеш из @lru_cache)
    expression = prepare_expression(expression).strip()
    
    # Этап 2: Валидация - проверка на пустоту
    if not expression:
        raise ValueError("Пусто вираз")
    
    # Этап 3: Создание окружения для вычисления
    env = SAFE_NAMESPACE.copy()
    if variables:
        env.update(variables)
    
    # Этап 4: Безопасное вычисление
    try:
        # eval() с отключенными __builtins__ для безопасности
        # Работает только с функциями из SAFE_NAMESPACE
        result = eval(expression, {"__builtins__": None}, env)
        
        # Кешируем результат если это простое выражение
        if not variables:
            _EVAL_CACHE[_cache_key_from_expr_vars(expression)] = result
            # Ограничиваем размер кеша
            if len(_EVAL_CACHE) > _MAX_CACHE_SIZE:
                # Удаляем самый старый элемент (FIFO)
                _EVAL_CACHE.pop(next(iter(_EVAL_CACHE)))
        
        return result
    
    except ZeroDivisionError:
        raise ValueError("Ділення на нуль")
    except ValueError as e:
        raise ValueError(str(e)) from e
    except Exception as e:
        raise ValueError(f"Помилка обчислення: {str(e)}") from e


def clear_cache():
    """
    Очистить внутренние кеши для освобождения памяти
    
    Полезно вызывать если калькулятор работает долго.
    
    Example:
        >>> clear_cache()  # Очистить оба кеша
    """
    global _EVAL_CACHE
    _EVAL_CACHE.clear()
    prepare_expression.cache_clear()
    
    
def get_cache_stats():
    """
    Получить статистику кеширования для отладки
    
    Returns:
        dict: Информация о размере и использовании кешей
    
    Example:
        >>> stats = get_cache_stats()
        >>> print(f"Результатов в кеше: {stats['eval_cache_size']}")
    """
    return {
        "eval_cache_size": len(_EVAL_CACHE),
        "eval_cache_max": _MAX_CACHE_SIZE,
        "prepare_expr_cache_info": prepare_expression.cache_info()._asdict(),
    }
