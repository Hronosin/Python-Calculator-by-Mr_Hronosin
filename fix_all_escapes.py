#!/usr/bin/env python3
"""Скрипт для исправления escape-последовательностей во всех модулях"""

import os
import re

# Список файлов для исправления
files_to_fix = [
    'calculator/core/engine.py',
    'calculator/converters/__init__.py',
    'calculator/tools/__init__.py',
    'calculator/localization/__init__.py',
    'calculator/history/__init__.py',
    'calculator/utils/__init__.py',
    'calculator/ui/__init__.py',
]

for filepath in files_to_fix:
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Сохраняем оригинал для сравнения
            original = content
            
            # Заменяем \\" на " (убираем экранирование)
            # В raw string \\" это литерально обратный слеш + кавычка
            content = content.replace('\\"', '"')
            
            # Если есть изменения - пишем обратно
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'✓ Исправлен {filepath}')
            else:
                print(f'  {filepath} - нет изменений')
        except Exception as e:
            print(f'✗ Ошибка в {filepath}: {e}')
    else:
        print(f'✗ Файл не найден: {filepath}')

print('\nЗавершено')
