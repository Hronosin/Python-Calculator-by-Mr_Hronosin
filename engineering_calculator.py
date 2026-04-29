"""
Инженерный калькулятор на PyQt5
Запуск: python engineering_calculator.py
Зависимости: pip install PyQt5
"""

import ast
import sys
import math
import os
import json
from decimal import Decimal, InvalidOperation, getcontext
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QSizePolicy, QFrame, QListWidget, QListWidgetItem,
    QMenuBar, QMenu, QAction, QMessageBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from units_converter import UnitsConverter
from extended_mode import ExtendedModeDialog

# ─── Конфигурация ─────────────────────────────────────────────────────────────
LANGUAGE = os.getenv('CALC_LANG', 'ru')
CURRENT_THEME = 'dark'
EXTENDED_MODE_ENABLED = False
EXTENDED_MODE_FILE = os.path.join(os.path.dirname(__file__), 'extended_mode.txt')
getcontext().prec = 50

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
        'ukrainian': 'Українська',
        'distance': 'Длина',
        'weight': 'Вес',
        'temperature': 'Температура',
        'time': 'Время',
        'volume': 'Объём',
        'area': 'Площадь',
        'speed': 'Скорость',
        'energy': 'Энергия',
        'pressure': 'Давление',
        'force': 'Сила',
        'from': 'От',
        'to': 'К',
        'meter': 'метр',
        'kilometer': 'километр',
        'centimeter': 'сантиметр',
        'millimeter': 'миллиметр',
        'micrometer': 'микрометр',
        'nanometer': 'нанометр',
        'inch': 'дюйм',
        'foot': 'фут',
        'yard': 'ярд',
        'mile': 'миля',
        'nautical_mile': 'морская миля',
        'kilogram': 'килограмм',
        'gram': 'грамм',
        'milligram': 'миллиграмм',
        'microgram': 'микрограмм',
        'pound': 'фунт',
        'ounce': 'унция',
        'stone': 'стоун',
        'tonne': 'тонна',
        'celsius': 'градус Цельсия',
        'fahrenheit': 'градус Фаренгейта',
        'kelvin': 'кельвин',
        'second': 'секунда',
        'millisecond': 'миллисекунда',
        'microsecond': 'микросекунда',
        'nanosecond': 'наносекунда',
        'minute': 'минута',
        'hour': 'час',
        'day': 'день',
        'week': 'неделя',
        'year': 'год',
        'liter': 'литр',
        'milliliter': 'миллилитр',
        'microliter': 'микроли́тр',
        'cubic_meter': 'кубический метр',
        'cubic_centimeter': 'кубический сантиметр',
        'cubic_inch': 'кубический дюйм',
        'cubic_kilometer': 'кубический километр',
        'gallon': 'галлон',
        'pint': 'пинта',
        'fluid_ounce': 'жидкая унция',
        'square_meter': 'квадратный метр',
        'square_kilometer': 'квадратный километр',
        'square_centimeter': 'квадратный сантиметр',
        'square_millimeter': 'квадратный миллиметр',
        'square_inch': 'квадратный дюйм',
        'square_foot': 'квадратный фут',
        'square_yard': 'квадратный ярд',
        'acre': 'акр',
        'hectare': 'гектар',
        'square_mile': 'квадратная миля',
        'meter_per_second': 'метр в секунду',
        'kilometer_per_hour': 'километр в час',
        'mile_per_hour': 'миля в час',
        'knot': 'узел',
        'foot_per_second': 'фут в секунду',
        'joule': 'джоуль',
        'kilojoule': 'килоджоуль',
        'megajoule': 'мегаджоуль',
        'calorie': 'калория',
        'kilocalorie': 'килокалория',
        'watt_hour': 'ватт-час',
        'kilowatt_hour': 'киловатт-час',
        'electronvolt': 'электронвольт',
        'btu': 'британская тепловая единица',
        'pascal': 'паскаль',
        'kilopascal': 'килопаскаль',
        'hectopascal': 'гектопаскаль',
        'bar': 'бар',
        'atmosphere': 'атмосфера',
        'millimeter_of_mercury': 'миллиметр ртутного столба',
        'psi': 'фунт на квадратный дюйм',
        'newton': 'ньютон',
        'kilonewton': 'килоньюто́н',
        'dyne': 'дин',
        'kilogram_force': 'килограмм-сила',
        'pound_force': 'фунт-сила',
        'poundal': 'паундаль',
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
        'cot': 'ctg',
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
        'units': 'Конвертер',
        'units_title': 'Конвертер единиц',
        'extended_mode': 'Расширенный режим',
        'extended_mode_title': 'Расширенный режим',
        'extended_precision_mode': 'Расширенная точность',
        'open_extended_mode': 'Открыть расширенный режим',
        'search_formulas': 'Поиск формул',
        'sort_az': 'A→Z',
        'sort_za': 'Z→A',
        'pro_mode': 'Pro Mode',
        'pro_mode_title': 'Pro Mode - Инструменты разработчика',
        'semiconductor_tab': 'Полупроводник',
        'bit_calc_tab': 'Битовый расчёт',
        'color_tab': 'Цвет',
        'base_conv_tab': 'Конвертер базы',
        'developer_tab': 'Dev Tools',
        'hash_tab': 'Хеш/CRC',
        'semiconductor_title': 'Время жизни полупроводника (уравнение Аррениуса)',
        'usage_time': 'Время использования (ч):',
        'current_label': 'Ток (A):',
        'junction_temp': 'Температура переходов (°C):',
        'ambient_temp': 'Температура окружающей среды (°C):',
        'theta_ja': 'Θ J-Ambient (°C/W):',
        'mtbf_label': 'MTBF @ 25°C (ч):',
        'activation_energy': 'Энергия активации Ea (эВ):',
        'bit_calc_title': 'Битовый калькулятор',
        'decimal_label': 'Десятичная:',
        'hex_label': 'Шестнадцатеричная:',
        'binary_label': 'Двоичная:',
        'octal_label': 'Восьмеричная:',
        'bit_count': 'Количество битов (1s):',
        'msb_pos': 'Позиция MSB:',
        'color_conv_title': 'Конвертер цветов',
        'hex_color': 'HEX:',
        'rgb_color': 'RGB:',
        'hsl_color': 'HSL:',
        'color_preview': 'Предпросмотр:',
        'base_conv_title': 'Конвертер базы',
        'input_base': 'Входная база:',
        'input_label': 'Ввод:',
        'decimal_output': 'Десятичная:',
        'binary_output': 'Двоичная:',
        'octal_output': 'Восьмеричная:',
        'hex_output': 'Шестнадцатеричная:',
        'hash_title': 'Хеш & CRC',
        'input_text': 'Входной текст:',
        'md5_label': 'MD5:',
        'sha1_label': 'SHA1:',
        'sha256_label': 'SHA256:',
        'crc32_label': 'CRC32:',
        'base64_label': 'Base64:',

        'formula_select': 'Формула',
        'formula_expression': 'Выражение',
        'compute': 'Вычислить',
        'result': 'Результат',
        'precision_note': 'Высокая точность до 30 знаков после запятой',
        'byte_count_label': 'Байт',
        'bytes_label': 'байт',
        'bit_width_label': 'Разрядность:',
        'signed_mode_label': 'Режим:',
        'signed_option': 'Знаковое',
        'unsigned_option': 'Беззнаковое',
        'integer_conversion_title': 'Целочисленные операции',
        'timestamp_title': 'Unix Время',
        'integer_input_label': 'Значение:',
        'integer_base_label': 'База ввода:',
        'integer_width_label': 'Разрядность:',
        'integer_range_label': 'Диапазон:',
        'two_complement_label': 'Двоичное доп.:',
        'epoch_input_label': 'Epoch (сек):',
        'datetime_input_label': 'Дата/время:',
        'epoch_seconds_label': 'Epoch секунд:',
        'epoch_milliseconds_label': 'Epoch мс:',
        'iso_datetime_label': 'ISO Время:',
        'developer_tools_title': 'Инструменты разработчика',
        'developer_tab': 'Dev Tools',
        'graphing_tab': 'Графики',
        'matrix_tab': 'Матрицы',
        'equation_solver_tab': 'Решатель уравнений',
        'statistics_tab': 'Статистика',
        'complex_tab': 'Комплексные',

        'function_label': 'Функция:',
        'plot_button': 'Построить',
        'x_range_label': 'Диапазон X:',
        'from_label': 'От:',
        'to_label': 'До:',

        'matrix_a_label': 'Матрица A:',
        'matrix_b_label': 'Матрица B:',
        'add_button': 'Сложить',
        'multiply_button': 'Умножить',
        'determinant_button': 'Детерминант',
        'result_label': 'Результат:',

        'equations_label': 'Уравнения:',
        'solve_button': 'Решить',
        'variables_label': 'Переменные:',

        'data_label': 'Данные:',
        'mean_button': 'Среднее',
        'std_button': 'Стд отклонение',
        'regression_button': 'Регрессия',

        'median_button': 'Медиана',
        'mode_button': 'Мода',

        'complex_a_label': 'Комплекс A:',
        'complex_b_label': 'Комплекс B:',
        'complex_op_label': 'Операция:',
        'add_op': 'Сложить',
        'sub_op': 'Вычесть',
        'mul_op': 'Умножить',
        'div_op': 'Разделить',
        'calculate_button': 'Вычислить',

        'conjugate_op': 'Сопряженное',
        'abs_op': 'Модуль',

        'advanced_mode': 'Расширенный режим',

        'voltage_label': 'Напряжение (V):',
        'power_label': 'Мощность (W):',

        'current': 'Ток',
        'resistance': 'Сопротивление',
        'mass': 'Масса',
        'velocity': 'Скорость',
        'amount_substance': 'Количество вещества',
        'temperature': 'Температура',
        'gas_volume': 'Объём газа',
        'formula_ohms_law': 'Закон Ома',
        'formula_kinetic_energy': 'Кинетическая энергия',
        'formula_ideal_gas_law': 'Уравнение Менделеева–Клапейрона',
        'formula_mass_energy': 'Энергия массы',
        'formula_molar_concentration': 'Молярная концентрация',
        'formula_acceleration': 'Ускорение',
        'formula_pressure_force': 'Давление от силы',
        'formula_density': 'Плотность',
        'formula_gravitational_force': 'Гравитационная сила',
        'formula_potential_energy': 'Потенциальная энергия',
        'formula_spring_energy': 'Энергия пружины',
        'formula_wave_energy': 'Энергия волны',
        'formula_work': 'Работа',
        'formula_heat_capacity': 'Теплоёмкость',
        'formula_power': 'Мощность',
        'formula_ph': 'pH',
        'formula_electrical_power': 'Электрическая мощность',
        'formula_electrical_energy': 'Электрическая энергия',
        'formula_joule_heat': 'Джоулева теплота',
        'formula_coulombs_law': 'Закон Кулона',
        'formula_electric_field': 'Электрическое поле',
        'formula_capacitance': 'Ёмкость',
        'formula_capacitor_energy': 'Энергия конденсатора',
        'formula_rc_time_constant': 'Постоянная времени RC',
        'formula_conductance': 'Проводимость',
        'formula_voltage_divider': 'Делитель напряжения',
        'formula_magnetic_force': 'Магнитная сила',
        'formula_inductance_energy': 'Энергия катушки',
        'formula_charge_flow': 'Поток заряда',
        'formula_power_dissipation': 'Рассеивание мощности',
        'formula_magnetic_field_wire': 'Магнитное поле провода',
        'sort_az': 'Сортировать A–Z',
        'sort_za': 'Сортировать Z–A',
        'formula_newtons_second_law': 'Второй закон Ньютона',
        'formula_momentum': 'Импульс',
        'formula_impulse': 'Импульс силы',
        'formula_pressure': 'Давление',
        'formula_buoyant_force': 'Выталкивающая сила',
        'formula_wave_speed': 'Скорость волны',
        'formula_frequency_from_period': 'Частота по периоду',
        'formula_impact_velocity': 'Скорость падения',
        'formula_centripetal_force': 'Центростремительная сила',
        'formula_force_velocity_power': 'Мощность от силы и скорости',
        'formula_hydrostatic_pressure': 'Гидростатическое давление',
        'formula_escape_velocity': 'Первоначальная скорость',
        'formula_magnetic_flux': 'Магнитный поток',
        'formula_parallel_plate_capacitance': 'Ёмкость плоского конденсатора',
        'formula_material_resistance': 'Сопротивление материала',
        'formula_stefan_boltzmann': 'Закон Стефана-Больцмана',
        'formula_de_broglie_wavelength': 'Де-Бройль длина волны',
        'formula_photon_energy': 'Энергия фотона',
        'formula_kinetic_energy_momentum': 'Кинетическая энергия через импульс',
        'formula_lens_focal_length': 'Фокусное расстояние линзы',
        'height': 'Высота',
        'frequency': 'Частота',
        'momentum': 'Импульс',
        'period': 'Период',
        'permittivity': 'Диэлектрическая проницаемость',
        'resistivity': 'Удельное сопротивление',
        'object_distance': 'Дистанция объекта',
        'image_distance': 'Дистанция изображения',
        'spring_constant': 'Жёсткость пружины',
        'volume_liters': 'Объём (л)',
        'specific_heat_capacity': 'Удельная теплоёмкость',
        'temperature_change': 'Изменение температуры',
        'wavelength': 'Длина волны',
        'hydrogen_ion_concentration': 'Концентрация ионов водорода',
        'work': 'Работа',
        'voltage': 'Напряжение',
        'power': 'Мощность',
        'charge': 'Заряд',
        'charge_1': 'Заряд 1',
        'charge_2': 'Заряд 2',
        'capacitance': 'Ёмкость',
        'input_voltage': 'Входное напряжение',
        'resistance_1': 'Сопротивление 1',
        'resistance_2': 'Сопротивление 2',
        'magnetic_field': 'Магнитное поле',
        'length': 'Длина',
        'inductance': 'Индуктивность',
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
        'ukrainian': 'Ukrainian',
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
        'from': 'From',
        'to': 'To',
        'meter': 'Meter',
        'kilometer': 'Kilometer',
        'centimeter': 'Centimeter',
        'millimeter': 'Millimeter',
        'micrometer': 'Micrometer',
        'nanometer': 'Nanometer',
        'inch': 'Inch',
        'foot': 'Foot',
        'yard': 'Yard',
        'mile': 'Mile',
        'nautical_mile': 'Nautical mile',
        'kilogram': 'Kilogram',
        'gram': 'Gram',
        'milligram': 'Milligram',
        'microgram': 'Microgram',
        'pound': 'Pound',
        'ounce': 'Ounce',
        'stone': 'Stone',
        'tonne': 'Tonne',
        'celsius': 'Celsius',
        'fahrenheit': 'Fahrenheit',
        'kelvin': 'Kelvin',
        'second': 'Second',
        'millisecond': 'Millisecond',
        'microsecond': 'Microsecond',
        'nanosecond': 'Nanosecond',
        'minute': 'Minute',
        'hour': 'Hour',
        'day': 'Day',
        'week': 'Week',
        'year': 'Year',
        'liter': 'Liter',
        'milliliter': 'Milliliter',
        'microliter': 'Microliter',
        'cubic_meter': 'Cubic meter',
        'cubic_centimeter': 'Cubic centimeter',
        'cubic_inch': 'Cubic inch',
        'cubic_kilometer': 'Cubic kilometer',
        'gallon': 'Gallon',
        'pint': 'Pint',
        'fluid_ounce': 'Fluid ounce',
        'square_meter': 'Square meter',
        'square_kilometer': 'Square kilometer',
        'square_centimeter': 'Square centimeter',
        'square_millimeter': 'Square millimeter',
        'square_inch': 'Square inch',
        'square_foot': 'Square foot',
        'square_yard': 'Square yard',
        'acre': 'Acre',
        'hectare': 'Hectare',
        'square_mile': 'Square mile',
        'meter_per_second': 'Meter per second',
        'kilometer_per_hour': 'Kilometer per hour',
        'mile_per_hour': 'Mile per hour',
        'knot': 'Knot',
        'foot_per_second': 'Foot per second',
        'joule': 'Joule',
        'kilojoule': 'Kilojoule',
        'megajoule': 'Megajoule',
        'calorie': 'Calorie',
        'kilocalorie': 'Kilocalorie',
        'watt_hour': 'Watt-hour',
        'kilowatt_hour': 'Kilowatt-hour',
        'electronvolt': 'Electronvolt',
        'btu': 'British thermal unit',
        'pascal': 'Pascal',
        'kilopascal': 'Kilopascal',
        'hectopascal': 'Hectopascal',
        'bar': 'Bar',
        'atmosphere': 'Atmosphere',
        'millimeter_of_mercury': 'Millimeter of mercury',
        'psi': 'Pound per square inch',
        'newton': 'Newton',
        'kilonewton': 'Kilonewton',
        'dyne': 'Dyne',
        'kilogram_force': 'Kilogram-force',
        'pound_force': 'Pound-force',
        'poundal': 'Poundal',
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
        'cot': 'cot',
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
        'units': 'Converter',
        'units_title': 'Unit Converter',
        'extended_mode': 'Extended Mode',
        'extended_mode_title': 'Extended Mode',
        'extended_precision_mode': 'High precision mode',
        'open_extended_mode': 'Open Extended Mode',
        'search_formulas': 'Search formulas',
        'pro_mode': 'Pro Mode',
        'pro_mode_title': 'Pro Mode - Developer Tools',
        'semiconductor_tab': 'Semiconductor',
        'bit_calc_tab': 'Bit Calc',
        'color_tab': 'Color',
        'base_conv_tab': 'Base Conv',
        'hash_tab': 'Hash/CRC',
        'semiconductor_title': 'Semiconductor Lifetime (Arrhenius Equation)',
        'usage_time': 'Usage time (h):',
        'current_label': 'Current (A):',
        'junction_temp': 'Junction Temp (°C):',
        'ambient_temp': 'Ambient Temp (°C):',
        'theta_ja': 'Θ J-Ambient (°C/W):',
        'mtbf_label': 'MTBF @ 25°C (h):',
        'activation_energy': 'Activation Energy Ea (eV):',
        'bit_calc_title': 'Bit Calculator',
        'decimal_label': 'Decimal:',
        'hex_label': 'Hexadecimal:',
        'binary_label': 'Binary:',
        'octal_label': 'Octal:',
        'bit_count': 'Bit count (1s):',
        'msb_pos': 'MSB position:',
        'color_conv_title': 'Color Converter',
        'hex_color': 'HEX:',
        'rgb_color': 'RGB:',
        'hsl_color': 'HSL:',
        'color_preview': 'Preview:',
        'base_conv_title': 'Base Converter',
        'input_base': 'Input base:',
        'input_label': 'Input:',
        'decimal_output': 'Decimal:',
        'binary_output': 'Binary:',
        'octal_output': 'Octal:',
        'hex_output': 'Hex:',
        'hash_title': 'Hash & CRC',
        'input_text': 'Input text:',
        'md5_label': 'MD5:',
        'sha1_label': 'SHA1:',
        'sha256_label': 'SHA256:',
        'crc32_label': 'CRC32:',
        'base64_label': 'Base64:',
        'byte_count_label': 'Bytes',
        'bytes_label': 'bytes',
        'bit_width_label': 'Bit width:',
        'signed_mode_label': 'Mode:',
        'signed_option': 'Signed',
        'unsigned_option': 'Unsigned',
        'integer_conversion_title': 'Integer tools',
        'timestamp_title': 'Unix Time',
        'integer_input_label': 'Value:',
        'integer_base_label': 'Input base:',
        'integer_width_label': 'Bit width:',
        'integer_range_label': 'Range:',
        'two_complement_label': 'Two’s complement:',
        'epoch_input_label': 'Epoch (sec):',
        'datetime_input_label': 'Date/time:',
        'epoch_seconds_label': 'Epoch seconds:',
        'epoch_milliseconds_label': 'Epoch ms:',
        'iso_datetime_label': 'ISO Time:',
        'developer_tools_title': 'Developer Tools',
        'developer_tab': 'Dev Tools',
        'graphing_tab': 'Graphing',
        'matrix_tab': 'Matrix',
        'equation_solver_tab': 'Equation Solver',
        'statistics_tab': 'Statistics',
        'complex_tab': 'Complex',

        'function_label': 'Function:',
        'plot_button': 'Plot',
        'x_range_label': 'X range:',
        'from_label': 'From:',
        'to_label': 'To:',

        'matrix_a_label': 'Matrix A:',
        'matrix_b_label': 'Matrix B:',
        'add_button': 'Add',
        'multiply_button': 'Multiply',
        'determinant_button': 'Determinant',
        'result_label': 'Result:',

        'equations_label': 'Equations:',
        'solve_button': 'Solve',
        'variables_label': 'Variables:',

        'data_label': 'Data:',
        'mean_button': 'Mean',
        'std_button': 'Std Dev',
        'regression_button': 'Regression',

        'median_button': 'Median',
        'mode_button': 'Mode',

        'complex_a_label': 'Complex A:',
        'complex_b_label': 'Complex B:',
        'complex_op_label': 'Operation:',
        'add_op': 'Add',
        'sub_op': 'Subtract',
        'mul_op': 'Multiply',
        'div_op': 'Divide',
        'calculate_button': 'Calculate',

        'conjugate_op': 'Conjugate',
        'abs_op': 'Absolute',

        'advanced_mode': 'Advanced Mode',

        'voltage_label': 'Voltage (V):',
        'power_label': 'Power (W):',

        'formula_select': 'Formula',
        'formula_expression': 'Expression',
        'compute': 'Compute',
        'result': 'Result',
        'precision_note': 'High precision up to 30 digits after decimal',
        'current': 'Current',
        'resistance': 'Resistance',
        'mass': 'Mass',
        'velocity': 'Velocity',
        'amount_substance': 'Amount of substance',
        'temperature': 'Temperature',
        'gas_volume': 'Gas volume',
        'formula_ohms_law': 'Ohm\'s law',
        'formula_kinetic_energy': 'Kinetic energy',
        'formula_ideal_gas_law': 'Ideal gas law',
        'formula_mass_energy': 'Mass-energy equivalence',
        'formula_molar_concentration': 'Molar concentration',
        'formula_acceleration': 'Acceleration',
        'formula_pressure_force': 'Pressure from force',
        'formula_density': 'Density',
        'formula_gravitational_force': 'Gravitational force',
        'formula_potential_energy': 'Potential energy',
        'formula_spring_energy': 'Spring energy',
        'formula_wave_energy': 'Wave energy',
        'formula_work': 'Work',
        'formula_heat_capacity': 'Heat capacity',
        'formula_power': 'Power',
        'formula_ph': 'pH',
        'formula_electrical_power': 'Electrical Power',
        'formula_electrical_energy': 'Electrical Energy',
        'formula_joule_heat': 'Joule Heat',
        'formula_coulombs_law': 'Coulomb\'s Law',
        'formula_electric_field': 'Electric Field',
        'formula_capacitance': 'Capacitance',
        'formula_capacitor_energy': 'Capacitor Energy',
        'formula_rc_time_constant': 'RC Time Constant',
        'formula_conductance': 'Conductance',
        'formula_voltage_divider': 'Voltage Divider',
        'formula_magnetic_force': 'Magnetic Force',
        'formula_inductance_energy': 'Inductance Energy',
        'formula_charge_flow': 'Charge Flow',
        'formula_power_dissipation': 'Power Dissipation',
        'formula_magnetic_field_wire': 'Magnetic Field (Wire)',
        'sort_az': 'Sort A–Z',
        'sort_za': 'Sort Z–A',
        'formula_newtons_second_law': 'Newton\'s second law',
        'formula_momentum': 'Momentum',
        'formula_impulse': 'Impulse',
        'formula_pressure': 'Pressure',
        'formula_buoyant_force': 'Buoyant force',
        'formula_wave_speed': 'Wave speed',
        'formula_frequency_from_period': 'Frequency from period',
        'formula_impact_velocity': 'Impact velocity',
        'formula_centripetal_force': 'Centripetal force',
        'formula_force_velocity_power': 'Force × velocity power',
        'formula_hydrostatic_pressure': 'Hydrostatic pressure',
        'formula_escape_velocity': 'Escape velocity',
        'formula_magnetic_flux': 'Magnetic flux',
        'formula_parallel_plate_capacitance': 'Parallel-plate capacitance',
        'formula_material_resistance': 'Material resistance',
        'formula_stefan_boltzmann': 'Stefan-Boltzmann law',
        'formula_de_broglie_wavelength': 'De Broglie wavelength',
        'formula_photon_energy': 'Photon energy',
        'formula_kinetic_energy_momentum': 'Kinetic energy from momentum',
        'formula_lens_focal_length': 'Lens focal length',
        'height': 'Height',
        'frequency': 'Frequency',
        'momentum': 'Momentum',
        'period': 'Period',
        'permittivity': 'Permittivity',
        'resistivity': 'Resistivity',
        'object_distance': 'Object distance',
        'image_distance': 'Image distance',
        'spring_constant': 'Spring constant',
        'volume_liters': 'Volume (L)',
        'specific_heat_capacity': 'Specific heat capacity',
        'temperature_change': 'Temperature change',
        'wavelength': 'Wavelength',
        'hydrogen_ion_concentration': 'Hydrogen ion concentration',
        'work': 'Work',
        'voltage': 'Voltage',
        'power': 'Power',
        'charge': 'Charge',
        'charge_1': 'Charge 1',
        'charge_2': 'Charge 2',
        'capacitance': 'Capacitance',
        'input_voltage': 'Input Voltage',
        'resistance_1': 'Resistance 1',
        'resistance_2': 'Resistance 2',
        'magnetic_field': 'Magnetic Field',
        'length': 'Length',
        'inductance': 'Inductance',
    },
    'uk': {
        'window_title': 'Інженерний калькулятор',
        'file_menu': 'Файл',
        'exit': 'Вихід',
        'view_menu': 'Перегляд',
        'theme_menu': 'Тема',
        'dark_theme': 'Темна',
        'light_theme': 'Світла',
        'lang_menu': 'Мова',
        'russian': 'Російська',
        'english': 'Англійська',
        'ukrainian': 'Українська',
        'distance': 'Довжина',
        'weight': 'Вага',
        'temperature': 'Температура',
        'time': 'Час',
        'volume': 'Об’єм',
        'area': 'Площа',
        'speed': 'Швидкість',
        'energy': 'Енергія',
        'pressure': 'Тиск',
        'force': 'Сила',
        'from': 'Від',
        'to': 'До',
        'meter': 'метр',
        'kilometer': 'кілометр',
        'centimeter': 'сантиметр',
        'millimeter': 'міліметр',
        'micrometer': 'мікрометр',
        'nanometer': 'нанометр',
        'inch': 'дюйм',
        'foot': 'фут',
        'yard': 'ярд',
        'mile': 'міля',
        'nautical_mile': 'морська миля',
        'kilogram': 'кілограм',
        'gram': 'грам',
        'milligram': 'міліграм',
        'microgram': 'мікрограм',
        'pound': 'фунт',
        'ounce': 'унція',
        'stone': ' стоун',
        'tonne': 'тонна',
        'celsius': 'градус Цельсія',
        'fahrenheit': 'градус Фаренгейта',
        'kelvin': 'кельвін',
        'second': 'секунда',
        'millisecond': 'мілісекунда',
        'microsecond': 'мікросекунда',
        'nanosecond': 'наносекунда',
        'minute': 'хвилина',
        'hour': 'година',
        'day': 'день',
        'week': 'тиждень',
        'year': 'рік',
        'liter': 'літр',
        'milliliter': 'мілілітр',
        'microliter': 'мікролітр',
        'cubic_meter': 'кубічний метр',
        'cubic_centimeter': 'кубічний сантиметр',
        'cubic_inch': 'кубічний дюйм',
        'cubic_kilometer': 'кубічний кілометр',
        'gallon': 'галон',
        'pint': 'пінта',
        'fluid_ounce': 'жидка унція',
        'square_meter': 'квадратний метр',
        'square_kilometer': 'квадратний кілометр',
        'square_centimeter': 'квадратний сантиметр',
        'square_millimeter': 'квадратний міліметр',
        'square_inch': 'квадратний дюйм',
        'square_foot': 'квадратний фут',
        'square_yard': 'квадратний ярд',
        'acre': 'акр',
        'hectare': 'гектар',
        'square_mile': 'квадратна миля',
        'meter_per_second': 'метр на секунду',
        'kilometer_per_hour': 'кілометр на годину',
        'mile_per_hour': 'миля на годину',
        'knot': 'вузол',
        'foot_per_second': 'фут на секунду',
        'joule': 'джоуль',
        'kilojoule': 'кілоджоуль',
        'megajoule': 'мегаджоуль',
        'calorie': 'калорія',
        'kilocalorie': 'кілокалорія',
        'watt_hour': 'ват-година',
        'kilowatt_hour': 'кіловат-година',
        'electronvolt': 'електронвольт',
        'btu': 'британська термальна одиниця',
        'pascal': 'паскаль',
        'kilopascal': 'кілопаскаль',
        'hectopascal': 'гектопаскаль',
        'bar': 'бар',
        'atmosphere': 'атмосфера',
        'millimeter_of_mercury': 'міліметр ртутного стовпа',
        'psi': 'фунт на квадратний дюйм',
        'newton': 'ньютон',
        'kilonewton': 'кілоньютон',
        'dyne': 'дин',
        'kilogram_force': 'кілограм-сила',
        'pound_force': 'фунт-сила',
        'poundal': 'паундаль',
        'restart_required': 'Потрібно перезапустити для застосування змін',
        'history_title': 'Історія',
        'clear_history': 'очистити',
        'error': 'Помилка',
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
        'cot': 'ctg',
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
        'units': 'Конвертер',
        'units_title': 'Конвертер одиниць',
        'extended_mode': 'Розширений режим',
        'extended_mode_title': 'Розширений режим',
        'extended_precision_mode': 'Розширена точність',
        'open_extended_mode': 'Відкрити розширений режим',
        'search_formulas': 'Пошук формул',
        'pro_mode': 'Pro Mode',
        'pro_mode_title': 'Pro Mode - Інструменти розробника',
        'semiconductor_tab': 'Напівпровідник',
        'bit_calc_tab': 'Бітовий розрахунок',
        'color_tab': 'Колір',
        'base_conv_tab': 'Конвертер базисів',
        'hash_tab': 'Хеш/CRC',
        'semiconductor_title': 'Час життя напівпровідника (рівняння Арреніуса)',
        'usage_time': 'Час використання (ч):',
        'current_label': 'Струм (A):',
        'junction_temp': 'Температура переходу (°C):',
        'ambient_temp': 'Температура навколишнього середовища (°C):',
        'theta_ja': 'Θ J-Ambient (°C/W):',
        'mtbf_label': 'MTBF @ 25°C (ч):',
        'activation_energy': 'Енергія активації Ea (еВ):',
        'bit_calc_title': 'Бітовий калькулятор',
        'decimal_label': 'Десяткова:',
        'hex_label': 'Шістнадцяткова:',
        'binary_label': 'Двійкова:',
        'octal_label': 'Вісімкова:',
        'bit_count': 'Кількість бітів (1s):',
        'msb_pos': 'Позиція MSB:',
        'color_conv_title': 'Конвертер кольорів',
        'hex_color': 'HEX:',
        'rgb_color': 'RGB:',
        'hsl_color': 'HSL:',
        'color_preview': 'Попередній перегляд:',
        'base_conv_title': 'Конвертер базисів',
        'input_base': 'Основа введення:',
        'input_label': 'Введення:',
        'decimal_output': 'Десяткова:',
        'binary_output': 'Двійкова:',
        'octal_output': 'Вісімкова:',
        'hex_output': 'Шістнадцяткова:',
        'hash_title': 'Хеш & CRC',
        'input_text': 'Вхідний текст:',
        'md5_label': 'MD5:',
        'sha1_label': 'SHA1:',
        'sha256_label': 'SHA256:',
        'crc32_label': 'CRC32:',
        'base64_label': 'Base64:',
        'byte_count_label': 'Байт',
        'bytes_label': 'байт',
        'bit_width_label': 'Розрядність:',
        'signed_mode_label': 'Режим:',
        'signed_option': 'Знакове',
        'unsigned_option': 'Беззнакове',
        'integer_conversion_title': 'Цілочисельні інструменти',
        'timestamp_title': 'Unix час',
        'integer_input_label': 'Значення:',
        'integer_base_label': 'Основа вводу:',
        'integer_width_label': 'Розрядність:',
        'integer_range_label': 'Діапазон:',
        'two_complement_label': 'Двійкове доповнення:',
        'epoch_input_label': 'Epoch (сек):',
        'datetime_input_label': 'Дата/час:',
        'epoch_seconds_label': 'Epoch секунд:',
        'epoch_milliseconds_label': 'Epoch мс:',
        'iso_datetime_label': 'ISO час:',
        'developer_tools_title': 'Інструменти розробника',
        'developer_tab': 'Dev Tools',
        'graphing_tab': 'Графіки',
        'matrix_tab': 'Матриці',
        'equation_solver_tab': 'Розв\'язувач рівнянь',
        'statistics_tab': 'Статистика',
        'complex_tab': 'Комплексні',

        'function_label': 'Функція:',
        'plot_button': 'Побудувати',
        'x_range_label': 'Діапазон X:',
        'from_label': 'Від:',
        'to_label': 'До:',

        'matrix_a_label': 'Матриця A:',
        'matrix_b_label': 'Матриця B:',
        'add_button': 'Додати',
        'multiply_button': 'Помножити',
        'determinant_button': 'Детермінант',
        'result_label': 'Результат:',

        'equations_label': 'Рівняння:',
        'solve_button': 'Розв\'язати',
        'variables_label': 'Змінні:',

        'data_label': 'Дані:',
        'mean_button': 'Середнє',
        'std_button': 'Стд відхилення',
        'regression_button': 'Регресія',

        'median_button': 'Медіана',
        'mode_button': 'Мода',

        'complex_a_label': 'Комплекс A:',
        'complex_b_label': 'Комплекс B:',
        'complex_op_label': 'Операція:',
        'add_op': 'Додати',
        'sub_op': 'Відняти',
        'mul_op': 'Помножити',
        'div_op': 'Поділити',
        'calculate_button': 'Обчислити',

        'conjugate_op': 'Спряжене',
        'abs_op': 'Модуль',

        'advanced_mode': 'Розширений режим',

        'voltage_label': 'Напруга (V):',
        'power_label': 'Потужність (W):',

        'formula_select': 'Формула',
        'formula_expression': 'Выраження',
        'compute': 'Обчислити',
        'result': 'Результат',
        'precision_note': 'Висока точність до 30 знаків після коми',
        'current': 'Струм',
        'resistance': 'Опір',
        'mass': 'Маса',
        'velocity': 'Швидкість',
        'amount_substance': 'Кількість речовини',
        'temperature': 'Температура',
        'gas_volume': 'Об’єм газу',
        'formula_ohms_law': 'Закон Ома',
        'formula_kinetic_energy': 'Кінетична енергія',
        'formula_ideal_gas_law': 'Рівняння Менделєєва–Клапейрона',
        'formula_mass_energy': 'Енергія маси',
        'formula_molar_concentration': 'Молярна концентрація',
        'formula_acceleration': 'Прискорення',
        'formula_pressure_force': 'Тиск від сили',
        'formula_density': 'Густина',
        'formula_gravitational_force': 'Гравітаційна сила',
        'formula_potential_energy': 'Потенціальна енергія',
        'formula_spring_energy': 'Енергія пружини',
        'formula_wave_energy': 'Енергія хвилі',
        'formula_work': 'Робота',
        'formula_heat_capacity': 'Теплоємність',
        'formula_power': 'Потужність',
        'formula_ph': 'pH',
        'height': 'Висота',
        'spring_constant': 'Жорсткість пружини',
        'volume_liters': 'Об’єм (л)',
        'specific_heat_capacity': 'Питома теплоємність',
        'temperature_change': 'Зміна температури',
        'wavelength': 'Довжина хвилі',
        'hydrogen_ion_concentration': 'Концентрація іонів водню',
        'work': 'Робота',
        'formula_electrical_power': 'Електрична потужність',
        'formula_electrical_energy': 'Електрична енергія',
        'formula_joule_heat': 'Джоулева теплота',
        'formula_coulombs_law': 'Закон Кулона',
        'formula_electric_field': 'Електричне поле',
        'formula_capacitance': 'Ємність',
        'formula_capacitor_energy': 'Енергія конденсатора',
        'formula_rc_time_constant': 'Постійна часу RC',
        'formula_conductance': 'Провідність',
        'formula_voltage_divider': 'Дільник напруги',
        'formula_magnetic_force': 'Магнітна сила',
        'formula_inductance_energy': 'Енергія котушки',
        'formula_charge_flow': 'Потік заряду',
        'formula_power_dissipation': 'Розсіювання потужності',
        'formula_magnetic_field_wire': 'Магнітне поле дроту',
        'sort_az': 'Сортувати A–Z',
        'sort_za': 'Сортувати Z–A',
        'formula_newtons_second_law': 'Другий закон Ньютона',
        'formula_momentum': 'Імпульс',
        'formula_impulse': 'Імпульс сили',
        'formula_pressure': 'Тиск',
        'formula_buoyant_force': 'Виштовхувальна сила',
        'formula_wave_speed': 'Швидкість хвилі',
        'formula_frequency_from_period': 'Частота за періодом',
        'formula_impact_velocity': 'Швидкість падіння',
        'formula_centripetal_force': 'Центростремна сила',
        'formula_force_velocity_power': 'Потужність від сили і швидкості',
        'formula_hydrostatic_pressure': 'Гідростатичний тиск',
        'formula_escape_velocity': 'Швидкість втечі',
        'formula_magnetic_flux': 'Магнітний потік',
        'formula_parallel_plate_capacitance': 'Ємність плоского конденсатора',
        'formula_material_resistance': 'Опір матеріалу',
        'formula_stefan_boltzmann': 'Закон Стефана-Больцмана',
        'formula_de_broglie_wavelength': 'Довжина хвилі Де Бройля',
        'formula_photon_energy': 'Енергія фотона',
        'formula_kinetic_energy_momentum': 'Кінетична енергія через імпульс',
        'formula_lens_focal_length': 'Фокусна відстань лінзи',
        'frequency': 'Частота',
        'momentum': 'Імпульс',
        'period': 'Період',
        'permittivity': 'Діелектрична проникність',
        'resistivity': 'Питомий опір',
        'object_distance': 'Відстань до об’єкта',
        'image_distance': 'Відстань до зображення',
        'voltage': 'Напруга',
        'power': 'Потужність',
        'charge': 'Заряд',
        'charge_1': 'Заряд 1',
        'charge_2': 'Заряд 2',
        'input_voltage': 'Вхідна напруга',
        'resistance_1': 'Опір 1',
        'resistance_2': 'Опір 2',
        'magnetic_field': 'Магнітне поле',
        'length': 'Довжина',
        'inductance': 'Індуктивність',
    }
}

THEMES = {
    'dark': {
        'DARK_BG': "#1a1a1f",
        'PANEL_BG': "#22222a",
        'CARD_BG': "#2b2b36",
        'CARD_HOVER': "#333340",
        'DISPLAY_BG': "#14141a",
        'TEXT_WHITE': "#eaeaf0",
        'TEXT_MUTED': "#8888a0",
        'TEXT_EXPR': "#5555aa",
        'ACCENT_BLUE': "#4a7cff",
        'ACCENT_GREEN': "#30d988",
        'ACCENT_AMBER': "#f5a623",
        'ACCENT_RED': "#ff5a5a",
        'BORDER': "#3a3a4a",
    },
    'light': {
        'DARK_BG': "#f5f5f5",
        'PANEL_BG': "#ffffff",
        'CARD_BG': "#e0e0e0",
        'CARD_HOVER': "#d0d0d0",
        'DISPLAY_BG': "#ffffff",
        'TEXT_WHITE': "#000000",
        'TEXT_MUTED': "#666666",
        'TEXT_EXPR': "#333333",
        'ACCENT_BLUE': "#0066cc",
        'ACCENT_GREEN': "#009900",
        'ACCENT_AMBER': "#ff9900",
        'ACCENT_RED': "#cc0000",
        'BORDER': "#cccccc",
    }
}

def get_text(key):
    return LOCALES.get(LANGUAGE, LOCALES['ru']).get(key, key)

def load_settings():
    global CURRENT_THEME, LANGUAGE, EXTENDED_MODE_ENABLED
    theme_file = os.path.join(os.path.dirname(__file__), 'theme.txt')
    lang_file = os.path.join(os.path.dirname(__file__), 'lang.txt')
    extended_file = os.path.join(os.path.dirname(__file__), 'extended_mode.txt')
    if os.path.exists(theme_file):
        try:
            with open(theme_file, 'r') as f:
                CURRENT_THEME = f.read().strip()
        except:
            pass
    if os.path.exists(lang_file):
        try:
            with open(lang_file, 'r') as f:
                LANGUAGE = f.read().strip()
        except:
            pass
    if os.path.exists(extended_file):
        try:
            with open(extended_file, 'r') as f:
                EXTENDED_MODE_ENABLED = f.read().strip() == '1'
        except:
            pass

def save_theme(theme):
    global CURRENT_THEME
    CURRENT_THEME = theme
    try:
        with open(os.path.join(os.path.dirname(__file__), 'theme.txt'), 'w') as f:
            f.write(theme)
    except:
        pass

def save_language(lang):
    global LANGUAGE
    LANGUAGE = lang
    try:
        with open(os.path.join(os.path.dirname(__file__), 'lang.txt'), 'w') as f:
            f.write(lang)
    except:
        pass

def save_extended_mode(enabled):
    global EXTENDED_MODE_ENABLED
    EXTENDED_MODE_ENABLED = bool(enabled)
    try:
        with open(EXTENDED_MODE_FILE, 'w') as f:
            f.write('1' if EXTENDED_MODE_ENABLED else '0')
    except:
        pass


def _decimal_literal_to_constructor(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return ast.copy_location(
            ast.Call(
                func=ast.Name(id='Decimal', ctx=ast.Load()),
                args=[ast.Constant(value=str(node.value))],
                keywords=[]
            ),
            node
        )
    return node


def _decimal_eval_expr(expr):
    try:
        tree = ast.parse(expr, mode='eval')
        class DecimalTransformer(ast.NodeTransformer):
            def visit_Constant(self, node):
                return _decimal_literal_to_constructor(node)
        tree = DecimalTransformer().visit(tree)
        tree = ast.fix_missing_locations(tree)
        compiled = compile(tree, '<decimal_eval>', 'eval')
        return eval(compiled, {'__builtins__': {}}, {'Decimal': Decimal})
    except Exception:
        raise

load_settings()
theme = THEMES[CURRENT_THEME]

# ─── Цветовая схема ────────────────────────────────────────────────────────────
DARK_BG      = theme['DARK_BG']
PANEL_BG     = theme['PANEL_BG']
CARD_BG      = theme['CARD_BG']
CARD_HOVER   = theme['CARD_HOVER']
DISPLAY_BG   = theme['DISPLAY_BG']
TEXT_WHITE   = theme['TEXT_WHITE']
TEXT_MUTED   = theme['TEXT_MUTED']
TEXT_EXPR    = theme['TEXT_EXPR']
ACCENT_BLUE  = theme['ACCENT_BLUE']
ACCENT_GREEN = theme['ACCENT_GREEN']
ACCENT_AMBER = theme['ACCENT_AMBER']
ACCENT_RED   = theme['ACCENT_RED']
BORDER       = theme['BORDER']

BTN_STYLES = {
    "num": {
        "bg": CARD_BG, "hover": CARD_HOVER,
        "fg": TEXT_WHITE, "size": 14
    },
    "op": {
        "bg": "#1f2a4a", "hover": "#263560",
        "fg": ACCENT_BLUE, "size": 15
    },
    "fn": {
        "bg": "#1e1e2a", "hover": "#28283a",
        "fg": TEXT_MUTED, "size": 12
    },
    "mem": {
        "bg": "#2a2215", "hover": "#38300a",
        "fg": ACCENT_AMBER, "size": 12
    },
    "eq": {
        "bg": ACCENT_BLUE, "hover": "#3a6aee",
        "fg": "#ffffff", "size": 18
    },
    "clr": {
        "bg": "#2a1515", "hover": "#3a1a1a",
        "fg": ACCENT_RED, "size": 13
    },
    "const": {
        "bg": "#152a1e", "hover": "#1c3828",
        "fg": ACCENT_GREEN, "size": 13
    },
    "mode": {
        "bg": "#252530", "hover": "#303040",
        "fg": TEXT_MUTED, "size": 11
    },
}


def make_btn(label: str, kind: str, w: int = 1, h: int = 1) -> QPushButton:
    s = BTN_STYLES[kind]
    btn = QPushButton(label)
    btn.setFont(QFont("Consolas", s["size"]))
    btn.setMinimumSize(QSize(52, 44))
    btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    bg, hov, fg = s["bg"], s["hover"], s["fg"]
    btn.setStyleSheet(f"""
        QPushButton {{
            background: {bg};
            color: {fg};
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 2px;
        }}
        QPushButton:hover {{ background: {hov}; }}
        QPushButton:pressed {{ background: {DARK_BG}; }}
    """)
    return btn


# ─── Главное окно ──────────────────────────────────────────────────────────────
class EngCalc(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(get_text('window_title'))
        self.setMinimumSize(680, 620)
        self.setStyleSheet(f"background: {DARK_BG};")

        # Состояние
        self.expr       = ""
        self.last_res   = None
        self.memory     = 0.0
        self.angle_mode = "DEG"   # DEG / RAD
        self.inv_mode   = False
        self.just_calc  = False
        self.history    = []

        self.load_history()
        self.load_state()
        self._build_ui()
        self._connect_keyboard()
        self._build_menu()

    # ── Построение UI ──────────────────────────────────────────────────────────
    def _build_ui(self):
        root = QWidget()
        root.setStyleSheet(f"background: {DARK_BG};")
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(10, 10, 10, 10)
        root_layout.setSpacing(10)

        # Левая колонка — основной калькулятор
        left = QWidget()
        lv = QVBoxLayout(left)
        lv.setContentsMargins(0, 0, 0, 0)
        lv.setSpacing(8)

        lv.addWidget(self._build_display())
        lv.addWidget(self._build_status_bar())
        lv.addWidget(self._build_buttons())

        # Правая колонка — история
        right = QWidget()
        right.setMinimumWidth(155)
        right.setMaximumWidth(195)
        rv = QVBoxLayout(right)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.setSpacing(4)
        rv.addWidget(self._build_history_panel())

        root_layout.addWidget(left, stretch=3)
        root_layout.addWidget(right, stretch=1)
        self.setCentralWidget(root)

    def _build_display(self):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {DISPLAY_BG};
                border: 1px solid {BORDER};
                border-radius: 12px;
            }}
        """)
        v = QVBoxLayout(frame)
        v.setContentsMargins(14, 10, 14, 10)
        v.setSpacing(2)

        self.lbl_expr = QLabel("")
        self.lbl_expr.setFont(QFont("Consolas", 11))
        self.lbl_expr.setStyleSheet(f"color: {TEXT_EXPR}; background: transparent; border: none;")
        self.lbl_expr.setAlignment(Qt.AlignRight)
        self.lbl_expr.setMinimumHeight(18)

        # Заменяем QLabel на QLineEdit для полного редактирования
        self.lbl_display = QLineEdit("0")
        self.lbl_display.setFont(QFont("Consolas", 28, QFont.Bold))
        self.lbl_display.setStyleSheet(f"""
            QLineEdit {{
                color: {TEXT_WHITE};
                background: transparent;
                border: none;
                padding: 5px;
            }}
            QLineEdit:focus {{ outline: none; }}
        """)
        self.lbl_display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_display.setMinimumHeight(46)
        # Подключаем сигналы для перехвата изменений
        self.lbl_display.textChanged.connect(self._on_display_changed)
        self.lbl_display.returnPressed.connect(self.calculate)
        self.lbl_display.setContextMenuPolicy(Qt.DefaultContextMenu)

        v.addWidget(self.lbl_expr)
        v.addWidget(self.lbl_display)
        return frame

    def _build_status_bar(self):
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(6)

        def badge(text, attr):
            lbl = QLabel(text)
            lbl.setFont(QFont("Consolas", 10))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedSize(46, 20)
            lbl.setStyleSheet(f"""
                color: {TEXT_MUTED}; background: {PANEL_BG};
                border: 1px solid {BORDER}; border-radius: 4px;
            """)
            setattr(self, attr, lbl)
            return lbl

        h.addWidget(badge(get_text('degrees'), "badge_deg"))
        h.addWidget(badge(get_text('radians'), "badge_rad"))
        h.addWidget(badge(get_text('memory'), "badge_mem"))
        h.addWidget(badge(get_text('inverse'), "badge_inv"))
        h.addStretch()
        self._update_badges()
        return w

    def _badge_on(self, lbl):
        lbl.setStyleSheet(f"""
            color: {ACCENT_BLUE}; background: #0d1a3a;
            border: 1px solid {ACCENT_BLUE}; border-radius: 4px;
        """)

    def _badge_off(self, lbl):
        lbl.setStyleSheet(f"""
            color: {TEXT_MUTED}; background: {PANEL_BG};
            border: 1px solid {BORDER}; border-radius: 4px;
        """)

    def _update_badges(self):
        if self.angle_mode == "DEG":
            self._badge_on(self.badge_deg);  self._badge_off(self.badge_rad)
        else:
            self._badge_off(self.badge_deg); self._badge_on(self.badge_rad)
        if self.memory != 0:
            self._badge_on(self.badge_mem)
        else:
            self._badge_off(self.badge_mem)
        if self.inv_mode:
            self._badge_on(self.badge_inv)
        else:
            self._badge_off(self.badge_inv)

    def _build_buttons(self):
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        g = QGridLayout(w)
        g.setSpacing(5)
        g.setContentsMargins(0, 0, 0, 0)

        def add(btn, r, c, rspan=1, cspan=1):
            g.addWidget(btn, r, c, rspan, cspan)

        # ── Строка 0: режимы и очистка ──────────────────────────────────────
        btn_angle = make_btn(get_text('deg_rad'), "mode")
        btn_angle.clicked.connect(self.toggle_angle)
        add(btn_angle, 0, 0)

        btn_inv = make_btn(get_text('inv_toggle'), "mode")
        btn_inv.clicked.connect(self.toggle_inv)
        add(btn_inv, 0, 1)

        btn_x2 = make_btn(get_text('square'), "fn")
        btn_x2.clicked.connect(lambda: self.apply_fn("pow2"))
        add(btn_x2, 0, 2)

        btn_xn = make_btn(get_text('power'), "fn")
        btn_xn.clicked.connect(lambda: self.input_str("**"))
        add(btn_xn, 0, 3)

        btn_pct = make_btn(get_text('pct'), "fn")
        btn_pct.clicked.connect(lambda: self.apply_fn("pct"))
        add(btn_pct, 0, 4)

        btn_ac = make_btn(get_text('clear'), "clr")
        btn_ac.clicked.connect(self.clear_all)
        add(btn_ac, 0, 5)

        # ── Строка 1: тригонометрия ────────────────────────────────────────
        for col, fn in enumerate(["sin", "cos", "tan", "log"]):
            b = make_btn(get_text(fn), "fn")
            b.clicked.connect(lambda _, f=fn: self.apply_fn(f))
            add(b, 1, col)

        btn_cot = make_btn(get_text('cot'), "fn")
        btn_cot.clicked.connect(lambda: self.apply_fn("cot"))
        add(btn_cot, 1, 4)

        btn_del = make_btn(get_text('delete'), "clr")
        btn_del.clicked.connect(self.del_last)
        add(btn_del, 1, 5)

        # ── Строка 2: гиперболические / доп. ─────────────────────────────
        for col, (key, fn) in enumerate([
            ("sinh","sinh"),("cosh","cosh"),("tanh","tanh"),
            ("log2","log2"),("exp","exp"),("ln","ln")
        ]):
            b = make_btn(get_text(key), "fn")
            b.clicked.connect(lambda _, f=fn: self.apply_fn(f))
            add(b, 2, col)

        # ── Строка 3: константы + доп. ────────────────────────────────────
        for col, (key, fn) in enumerate([
            ("pi","PI"),("e_const","E"),("phi","PHI"),
            ("sqrt","sqrt"),("fact","fact"),("cbrt","cbrt")
        ]):
            kind = "const" if col < 3 else "fn"
            b = make_btn(get_text(key), kind)
            if col < 3:
                b.clicked.connect(lambda _, c=fn: self.input_const(c))
            else:
                b.clicked.connect(lambda _, f=fn: self.apply_fn(f))
            add(b, 3, col)

        # ── Строка 4: память ─────────────────────────────────────────────
        for col, (key, fn) in enumerate([
            ("mc","mc"),("mr","mr"),("mplus","m+"),("mminus","m-"),
            ("inv","inv"),("floor","floor")
        ]):
            b = make_btn(get_text(key), "mem" if col < 4 else "fn")
            b.clicked.connect(lambda _, f=fn: self.mem_action(f))
            add(b, 4, col)

        # ── Строка 5: скобки и операции ──────────────────────────────────
        for col, (key, val) in enumerate([
            ("(","("), (")",")"), ("ee","e"),
            ("divide","/"),  ("multiply","*"), ("minus","-")
        ]):
            kind = "op" if col >= 3 else "fn"
            b = make_btn(get_text(key), kind)
            b.clicked.connect(lambda _, v=val: self.input_str(v))
            add(b, 5, col)

        # ── Цифровой блок ─────────────────────────────────────────────────
        digits_layout = [
            [("7",1),("8",1),("9",1),("−",1,"op"),("",0)],
        ]
        for col, dig in enumerate(["7", "8", "9"]):
            b = make_btn(dig, "num")
            b.clicked.connect(lambda _, d=dig: self.input_num(d))
            add(b, 6, col)

        btn_neg = make_btn(get_text('neg'), "fn")
        btn_neg.clicked.connect(self.toggle_sign)
        add(btn_neg, 6, 3)

        btn_plus = make_btn(get_text('plus'), "op")
        btn_plus.clicked.connect(lambda: self.input_str("+"))
        add(btn_plus, 6, 4, 2, 1)  # span 2 rows

        btn_mod = make_btn(get_text('modulo'), "fn")
        btn_mod.clicked.connect(lambda: self.input_str("%"))
        add(btn_mod, 6, 5)

        for col, dig in enumerate(["4", "5", "6"]):
            b = make_btn(dig, "num")
            b.clicked.connect(lambda _, d=dig: self.input_num(d))
            add(b, 7, col)

        btn_ceil = make_btn(get_text('ceil'), "fn")
        btn_ceil.clicked.connect(lambda: self.apply_fn("ceil"))
        add(btn_ceil, 7, 3)

        btn_rnd = make_btn(get_text('round'), "fn")
        btn_rnd.clicked.connect(lambda: self.apply_fn("round"))
        add(btn_rnd, 7, 5)

        for col, dig in enumerate(["1", "2", "3"]):
            b = make_btn(dig, "num")
            b.clicked.connect(lambda _, d=dig: self.input_num(d))
            add(b, 8, col)

        btn_eq = make_btn("=", "eq")
        btn_eq.clicked.connect(self.calculate)
        add(btn_eq, 8, 3, 1, 2)

        btn_cbrt = make_btn("∛x", "fn")
        btn_cbrt.clicked.connect(lambda: self.apply_fn("cbrt"))
        add(btn_cbrt, 8, 5)

        btn_0 = make_btn("0", "num")
        btn_0.clicked.connect(lambda: self.input_num("0"))
        add(btn_0, 9, 0, 1, 2)

        btn_dot = make_btn(get_text('dot'), "num")
        btn_dot.clicked.connect(self.input_dot)
        add(btn_dot, 9, 2)

        btn_pow10 = make_btn(get_text('pow10'), "fn")
        btn_pow10.clicked.connect(lambda: self.apply_fn("pow10"))
        add(btn_pow10, 9, 3)

        btn_ans = make_btn(get_text('ans'), "fn")
        btn_ans.clicked.connect(self.recall_ans)
        add(btn_ans, 9, 4)

        btn_pi2 = make_btn(get_text('pi_half'), "const")
        btn_pi2.clicked.connect(lambda: self.input_str(str(math.pi / 2)[:10]))
        add(btn_pi2, 9, 5)

        return w

    def _build_history_panel(self):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {PANEL_BG};
                border: 1px solid {BORDER};
                border-radius: 12px;
            }}
        """)
        v = QVBoxLayout(frame)
        v.setContentsMargins(8, 8, 8, 8)
        v.setSpacing(6)

        title_row = QHBoxLayout()
        lbl = QLabel(get_text('history_title'))
        lbl.setFont(QFont("Consolas", 11))
        lbl.setStyleSheet(f"color: {TEXT_MUTED}; background: transparent; border: none;")
        btn_clr = QPushButton(get_text('clear_history'))
        btn_clr.setFont(QFont("Consolas", 9))
        btn_clr.setStyleSheet(f"""
            QPushButton {{ color: {ACCENT_RED}; background: transparent; border: none; }}
            QPushButton:hover {{ color: #ff8888; }}
        """)
        btn_clr.clicked.connect(self.clear_history)
        title_row.addWidget(lbl)
        title_row.addStretch()
        title_row.addWidget(btn_clr)
        v.addLayout(title_row)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: {BORDER}; background: {BORDER};")
        sep.setFixedHeight(1)
        v.addWidget(sep)

        self.hist_list = QListWidget()
        self.hist_list.setStyleSheet(f"""
            QListWidget {{
                background: transparent;
                border: none;
                color: {TEXT_WHITE};
                font-family: Consolas;
                font-size: 11px;
            }}
            QListWidget::item {{ padding: 4px 2px; border-bottom: 1px solid {BORDER}; }}
            QListWidget::item:hover {{ background: {CARD_BG}; border-radius: 4px; }}
            QListWidget::item:selected {{ background: #1f2a4a; border-radius: 4px; }}
        """)
        self.hist_list.itemClicked.connect(self._recall_history)
        self._populate_history()
        v.addWidget(self.hist_list)
        return frame

    def _populate_history(self):
        self.hist_list.clear()
        for entry in self.history:
            item = QListWidgetItem(f"{entry['expr']}\n= {entry['val']}")
            item.setData(Qt.UserRole, entry['val'])
            self.hist_list.addItem(item)

    # ── Логика ─────────────────────────────────────────────────────────────────

    def _to_rad(self, x):
        return x * math.pi / 180 if self.angle_mode == "DEG" else x

    def _from_rad(self, x):
        return x * 180 / math.pi if self.angle_mode == "DEG" else x

    FN_MAP = {
        "sin":   lambda s, x: math.sin(s._to_rad(x)) if not s.inv_mode else s._from_rad(math.asin(x)),
        "cos":   lambda s, x: math.cos(s._to_rad(x)) if not s.inv_mode else s._from_rad(math.acos(x)),
        "tan":   lambda s, x: math.tan(s._to_rad(x)) if not s.inv_mode else s._from_rad(math.atan(x)),
        "cot":   lambda s, x: (1/math.tan(s._to_rad(x))) if not s.inv_mode else s._from_rad(math.atan(1/x)),
        "sinh":  lambda s, x: math.sinh(x)  if not s.inv_mode else math.asinh(x),
        "cosh":  lambda s, x: math.cosh(x)  if not s.inv_mode else math.acosh(x),
        "tanh":  lambda s, x: math.tanh(x)  if not s.inv_mode else math.atanh(x),
        "log":   lambda s, x: math.log10(x) if not s.inv_mode else 10**x,
        "ln":    lambda s, x: math.log(x)   if not s.inv_mode else math.exp(x),
        "log2":  lambda s, x: math.log2(x),
        "exp":   lambda s, x: math.exp(x),
        "sqrt":  lambda s, x: math.sqrt(x),
        "cbrt":  lambda s, x: x ** (1/3) if x >= 0 else -((-x) ** (1/3)),
        "pow2":  lambda s, x: x ** 2,
        "pow10": lambda s, x: 10 ** x,
        "abs":   lambda s, x: abs(x),
        "inv":   lambda s, x: 1 / x,
        "pct":   lambda s, x: s._smart_percentage(x),
        "floor": lambda s, x: math.floor(x),
        "ceil":  lambda s, x: math.ceil(x),
        "round": lambda s, x: round(x),
        "fact":  lambda s, x: float(math.factorial(int(x))),
    }

    CONST_MAP = {
        "PI":  math.pi,
        "E":   math.e,
        "PHI": (1 + math.sqrt(5)) / 2,
    }

    def _fmt(self, n):
        if isinstance(n, Decimal):
            if not n.is_finite():
                return str(n)
            if EXTENDED_MODE_ENABLED:
                quant = Decimal('1e-30')
                formatted = n.quantize(quant)
                s = format(formatted, 'f').rstrip('0').rstrip('.')
                return s or '0'
            else:
                n = float(n)
        if not math.isfinite(n):
            return str(n)
        if EXTENDED_MODE_ENABLED:
            d = Decimal(str(n))
            quant = Decimal('1e-30')
            formatted = d.quantize(quant)
            s = format(formatted, 'f').rstrip('0').rstrip('.')
            return s or '0'
        if abs(n) > 1e12 or (0 < abs(n) < 1e-7):
            return f"{n:.6e}"
        r = round(n, 12)
        s = f"{r:.12f}".rstrip("0").rstrip(".")
        return s

    def _smart_percentage(self, x):
        """Умная обработка процентов в контексте выражения"""
        return x / 100

    def _update_display(self, val=None, expr_text=""):
        """Обновляет дисплей с проверкой на редактирование"""
        if val is not None:
            self.lbl_display.setText(val)
        else:
            self.lbl_display.setText(self.expr or "0")
        self.lbl_expr.setText(expr_text)

    def _on_display_changed(self, text):
        """Синхронизирует выражение с содержимым поля"""
        self.expr = text
        self.just_calc = False

    def input_num(self, d):
        if self.just_calc:
            self.expr = ""; self.just_calc = False
        self.expr += d
        self._update_display(self.expr)

    def input_dot(self):
        if self.just_calc:
            self.expr = "0"; self.just_calc = False
        parts = self.expr.replace("**", " ").replace("*", " ").replace("/", " ") \
                         .replace("+", " ").replace("-", " ").split()
        last = parts[-1] if parts else ""
        if "." not in last:
            self.expr += "."
            self._update_display(self.expr)

    def input_str(self, s):
        """Умный ввод операторов и скобок"""
        # Если это оператор и последний символ тоже оператор, заменяем его
        if s in "+-*/" and self.expr and self.expr[-1] in "+-*/":
            self.expr = self.expr[:-1] + s
        elif s in "+-*/(" and self.just_calc:
            # Магия: после вычисления можно сразу продолжить с результатом
            self.expr += s
        else:
            self.expr += s
        
        if not self.expr.endswith(s):
            pass  # Уже добавили выше
        self.just_calc = False
        self._update_display(self.expr)

    def input_const(self, c):
        if self.just_calc:
            self.expr = ""; self.just_calc = False
        self.expr += str(self.CONST_MAP[c])[:12]
        self._update_display(self.expr)

    def toggle_sign(self):
        if not self.expr:
            return
        if self.expr.startswith("-"):
            self.expr = self.expr[1:]
        else:
            self.expr = "-" + self.expr
        self._update_display(self.expr)

    def apply_fn(self, fn):
        if not self.expr and self.last_res is not None:
            self.expr = self._fmt(self.last_res)
        if not self.expr:
            return
        
        # Специальная обработка для процентов
        if fn == "pct":
            self._apply_smart_percentage()
            return
        
        try:
            if EXTENDED_MODE_ENABLED:
                val = _decimal_eval_expr(self.expr)
                val_float = float(val)
            else:
                val = float(eval(self.expr, {"__builtins__": {}}, {}))
                val_float = val
            f = self.FN_MAP[fn]
            res = f(self, val_float)
            label = f"{fn}({self._fmt(val)})"
            self._add_history(label, res)
            self.last_res = res
            self.expr = self._fmt(res)
            self.just_calc = True
            self._update_display(self._fmt(res), label)
        except Exception as ex:
            self._update_display("Ошибка", str(ex))
    
    def _apply_smart_percentage(self):
        """Применяет проценты в контексте всего выражения"""
        try:
            # Ищем последний оператор и его позицию
            expr = self.expr
            last_op = None
            last_op_pos = -1
            
            for i, c in enumerate(reversed(expr)):
                if c in "+-*/" and i > 0:
                    last_op = c
                    last_op_pos = len(expr) - i - 1
                    break
            
            if last_op is None or last_op_pos <= 0:
                # Нет оператора, просто конвертируем в проценты
                if EXTENDED_MODE_ENABLED:
                    val = _decimal_eval_expr(expr)
                else:
                    val = float(eval(expr, {"__builtins__": {}}, {}))
                res = val / 100
                self._add_history(f"{expr}%", res)
                self.last_res = res
                self.expr = self._fmt(res)
                self.just_calc = True
                self._update_display(self._fmt(res), f"{expr}% =")
                return
            
            # Есть оператор, применяем проценты относительно левого операнда
            left_expr = expr[:last_op_pos]
            right_expr = expr[last_op_pos+1:]
            
            if EXTENDED_MODE_ENABLED:
                left_val = _decimal_eval_expr(left_expr)
                pct_val = _decimal_eval_expr(right_expr)
            else:
                left_val = float(eval(left_expr, {"__builtins__": {}}, {}))
                pct_val = float(eval(right_expr, {"__builtins__": {}}, {}))
            
            # Вычисляем процент от левого операнда
            pct_amount = (left_val * pct_val) / 100
            
            # Применяем операцию
            if last_op == "+":
                result = left_val + pct_amount
            elif last_op == "-":
                result = left_val - pct_amount
            elif last_op == "*":
                result = left_val * pct_amount
            elif last_op == "/":
                result = left_val / pct_amount if pct_amount != 0 else float('inf')
            
            label = f"{left_expr} {last_op} {right_expr}%"
            self._add_history(label, result)
            self.last_res = result
            self.expr = self._fmt(result)
            self.just_calc = True
            self._update_display(self._fmt(result), label + " =")
            
        except Exception as ex:
            self._update_display("Ошибка", str(ex))

    def calculate(self):
        if not self.expr:
            return
        orig = self.expr
        try:
            if EXTENDED_MODE_ENABLED:
                result = _decimal_eval_expr(self.expr)
                if not result.is_finite():
                    self._update_display(str(result), orig + " =")
                    return
            else:
                result = eval(self.expr, {"__builtins__": {}}, {})
                result = float(result)
                if not math.isfinite(result):
                    self._update_display(str(result), orig + " =")
                    return
            self._add_history(orig, result)
            self.last_res = result
            self._update_display(self._fmt(result), orig + " =")
            self.expr = self._fmt(result)
            self.just_calc = True
        except Exception:
            self._update_display("Ошибка", orig)

    def clear_all(self):
        self.expr = ""; self.last_res = None; self.just_calc = False
        self._update_display("0", "")

    def del_last(self):
        self.expr = self.expr[:-1]
        self._update_display(self.expr or "0")

    def recall_ans(self):
        if self.last_res is not None:
            if self.just_calc:
                self.expr = ""
                self.just_calc = False
            self.expr += self._fmt(self.last_res)
            self._update_display(self.expr)

    # ── Память ─────────────────────────────────────────────────────────────────
    def mem_action(self, act):
        if act == "mc":
            self.memory = 0.0
        elif act == "mr":
            if self.just_calc:
                self.expr = ""; self.just_calc = False
            self.expr += self._fmt(self.memory)
            self._update_display(self.expr)
        elif act in ("m+", "m-"):
            try:
                val = float(eval(self.expr, {"__builtins__": {}}, {})) if self.expr else 0
                self.memory += val if act == "m+" else -val
            except Exception:
                pass
        elif act == "inv":
            self.apply_fn("inv")
        elif act == "floor":
            self.apply_fn("floor")
        self._update_badges()

    # ── Угол и INV ─────────────────────────────────────────────────────────────
    def toggle_angle(self):
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        self._update_badges()

    def toggle_inv(self):
        self.inv_mode = not self.inv_mode
        self._update_badges()

    # ── История ────────────────────────────────────────────────────────────────
    def _add_history(self, expr_text, result):
        entry = {"expr": expr_text, "val": self._fmt(result)}
        self.history.insert(0, entry)
        if len(self.history) > 50:
            self.history.pop()
        self.save_history()
        item = QListWidgetItem(f"{expr_text}\n= {self._fmt(result)}")
        item.setData(Qt.UserRole, self._fmt(result))
        self.hist_list.insertItem(0, item)
        if self.hist_list.count() > 50:
            self.hist_list.takeItem(50)

    def _recall_history(self, item):
        val = item.data(Qt.UserRole)
        self.expr = val
        self.just_calc = False
        self._update_display(val)

    def clear_history(self):
        self.history.clear()
        self.hist_list.clear()
        self.save_history()

    # ── Клавиатура ─────────────────────────────────────────────────────────────
    def _connect_keyboard(self):
        pass  # обрабатывается через keyPressEvent

    def _build_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu(get_text('file_menu'))
        exit_action = QAction(get_text('exit'), self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        view_menu = menubar.addMenu(get_text('view_menu'))
        theme_menu = view_menu.addMenu(get_text('theme_menu'))
        dark_action = QAction(get_text('dark_theme'), self)
        dark_action.triggered.connect(lambda: self.change_theme('dark'))
        theme_menu.addAction(dark_action)
        light_action = QAction(get_text('light_theme'), self)
        light_action.triggered.connect(lambda: self.change_theme('light'))
        theme_menu.addAction(light_action)

        lang_menu = view_menu.addMenu(get_text('lang_menu'))
        ru_action = QAction(get_text('russian'), self)
        ru_action.triggered.connect(lambda: self.change_lang('ru'))
        lang_menu.addAction(ru_action)
        en_action = QAction(get_text('english'), self)
        en_action.triggered.connect(lambda: self.change_lang('en'))
        lang_menu.addAction(en_action)
        uk_action = QAction(get_text('ukrainian'), self)
        uk_action.triggered.connect(lambda: self.change_lang('uk'))
        lang_menu.addAction(uk_action)

        view_menu.addSeparator()
        self.extended_precision_action = QAction(get_text('extended_precision_mode'), self)
        self.extended_precision_action.setCheckable(True)
        self.extended_precision_action.setChecked(EXTENDED_MODE_ENABLED)
        self.extended_precision_action.toggled.connect(self.toggle_extended_mode)
        view_menu.addAction(self.extended_precision_action)

        open_extended_action = QAction(get_text('open_extended_mode'), self)
        open_extended_action.triggered.connect(self.show_extended_mode)
        view_menu.addAction(open_extended_action)

        units_action = QAction(get_text('units'), self)
        units_action.triggered.connect(self.show_units_converter)
        view_menu.addAction(units_action)

    def change_theme(self, theme_name):
        save_theme(theme_name)
        QMessageBox.information(self, get_text('window_title'), get_text('restart_required'))

    def change_lang(self, lang):
        save_language(lang)
        QMessageBox.information(self, get_text('window_title'), get_text('restart_required'))

    def show_units_converter(self):
        converter = UnitsConverter(self, theme, get_text)
        converter.exec_()

    def toggle_extended_mode(self, enabled):
        save_extended_mode(enabled)

    def show_extended_mode(self):
        dialog = ExtendedModeDialog(self, theme, get_text)
        dialog.exec_()

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()
        
        # Для фокуса на дисплее позволяем обычное редактирование
        if self.lbl_display.hasFocus():
            if key == Qt.Key_Return or key == Qt.Key_Enter:
                self.calculate()
                return
            elif key == Qt.Key_Backspace:
                # Позволяем стандартную обработку backspace в QLineEdit
                super().keyPressEvent(event)
                return
            elif key == Qt.Key_Escape:
                self.clear_all()
                return
            elif event.modifiers() & Qt.ControlModifier:
                if key == Qt.Key_A:
                    self.lbl_display.selectAll()
                    return
                super().keyPressEvent(event)
                return
            else:
                # Все остальные символы обрабатываются QLineEdit
                super().keyPressEvent(event)
                return
        
        # Обработка для кнопок (когда фокус не на дисплее)
        if text.isdigit():
            self.input_num(text)
        elif text == ".":
            self.input_dot()
        elif text in "+-*/":
            self.input_str(text)
        elif text == "(":
            self.input_str("(")
        elif text == ")":
            self.input_str(")")
        elif text == "^":
            self.input_str("**")
        elif text == "%":
            self.apply_fn("pct")
        elif key in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Equal):
            self.calculate()
        elif key == Qt.Key_Backspace:
            self.del_last()
        elif key == Qt.Key_Escape:
            self.clear_all()
        else:
            super().keyPressEvent(event)

    def save_history(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), 'history.json'), 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_history(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), 'history.json'), 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except:
            self.history = []

    def save_state(self):
        state = {
            'expr': self.expr,
            'last_res': self.last_res,
            'memory': self.memory,
            'angle_mode': self.angle_mode,
            'inv_mode': self.inv_mode,
            'just_calc': self.just_calc
        }
        try:
            with open(os.path.join(os.path.dirname(__file__), 'state.json'), 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_state(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), 'state.json'), 'r', encoding='utf-8') as f:
                state = json.load(f)
                self.expr = state.get('expr', '')
                self.last_res = state.get('last_res')
                self.memory = state.get('memory', 0.0)
                self.angle_mode = state.get('angle_mode', 'DEG')
                self.inv_mode = state.get('inv_mode', False)
                self.just_calc = state.get('just_calc', False)
        except:
            pass


# ─── Точка входа ───────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(DARK_BG))
    palette.setColor(QPalette.WindowText, QColor(TEXT_WHITE))
    app.setPalette(palette)

    win = EngCalc()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
