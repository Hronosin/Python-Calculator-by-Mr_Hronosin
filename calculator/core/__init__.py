"""
📦 Core Module (OPTIMIZED)
===========================

Ядро калькулятора содержит основные математические функции и движок вычисления с оптимизациями.

Модули:
    - engine.py: Основной движок расчётов с LRU кешем и оптимизациями
    - functions.py: Определение всех математических функций

Экспорт:
    - evaluate(): Основная функция вычисления выражений (с кешем)
    - SAFE_NAMESPACE: Безопасное пространство имён для eval()
    - clear_cache(): Очистить внутренние кеши
    - get_cache_stats(): Получить статистику кеширования
"""

from .engine import evaluate, SAFE_NAMESPACE, clear_cache, get_cache_stats

__all__ = ['evaluate', 'SAFE_NAMESPACE', 'clear_cache', 'get_cache_stats']
