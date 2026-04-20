import re

# Читаем файл
with open('calculator/ui/__init__.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем все \" на просто кавычку
# Это позволит избежать проблем с экранированием
lines = content.split('\n')
new_lines = []

for line in lines:
    # Заменяем \" на "  где это допустимо в docstrings и strings
    line = line.replace('\\"', '"')
    new_lines.append(line)

new_content = '\n'.join(new_lines)

# Пишем обратно
with open('calculator/ui/__init__.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✓ Fixed escape sequences")
