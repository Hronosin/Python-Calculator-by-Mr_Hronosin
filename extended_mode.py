"""Extended Mode for high-precision scientific and chemical calculations."""

from decimal import Decimal, InvalidOperation, getcontext
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QWidget, QFormLayout, QGroupBox, QSlider, QListWidget, QTabWidget,
    QComboBox, QTextEdit, QTableWidget, QTableWidgetItem, QSpinBox, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import math
import hashlib
import datetime
import binascii
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import statistics

getcontext().prec = 50

FORMULAS = [
    {
        'key': 'ohms_law',
        'label_key': 'formula_ohms_law',
        'expression': 'V = I × R',
        'unit': 'V',
        'params': [
            ('I', 'current', 'A'),
            ('R', 'resistance', 'Ω'),
        ],
        'compute': lambda values: values['I'] * values['R'],
    },
    {
        'key': 'kinetic_energy',
        'label_key': 'formula_kinetic_energy',
        'expression': 'E = 0.5 × m × v²',
        'unit': 'J',
        'params': [
            ('m', 'mass', 'kg'),
            ('v', 'velocity', 'm/s'),
        ],
        'compute': lambda values: Decimal('0.5') * values['m'] * values['v'] ** 2,
    },
    {
        'key': 'ideal_gas_law',
        'label_key': 'formula_ideal_gas_law',
        'expression': 'P = n × R × T / V',
        'unit': 'Pa',
        'params': [
            ('n', 'amount_substance', 'mol'),
            ('T', 'temperature', 'K'),
            ('V', 'gas_volume', 'm³'),
        ],
        'compute': lambda values: values['n'] * Decimal('8.31446261815324') * values['T'] / values['V'],
    },
    {
        'key': 'mass_energy',
        'label_key': 'formula_mass_energy',
        'expression': 'E = m × c²',
        'unit': 'J',
        'params': [
            ('m', 'mass', 'kg'),
        ],
        'compute': lambda values: values['m'] * Decimal('299792458') ** 2,
    },
    {
        'key': 'molar_concentration',
        'label_key': 'formula_molar_concentration',
        'expression': 'c = n / V',
        'unit': 'mol/L',
        'params': [
            ('n', 'amount_substance', 'mol'),
            ('V', 'volume_liters', 'L'),
        ],
        'compute': lambda values: values['n'] / values['V'],
    },
    {
        'key': 'acceleration',
        'label_key': 'formula_acceleration',
        'expression': 'a = F / m',
        'unit': 'm/s²',
        'params': [
            ('F', 'force', 'N'),
            ('m', 'mass', 'kg'),
        ],
        'compute': lambda values: values['F'] / values['m'],
    },
    {
        'key': 'density',
        'label_key': 'formula_density',
        'expression': 'ρ = m / V',
        'unit': 'kg/m³',
        'params': [
            ('m', 'mass', 'kg'),
            ('V', 'gas_volume', 'm³'),
        ],
        'compute': lambda values: values['m'] / values['V'],
    },
    {
        'key': 'gravitational_force',
        'label_key': 'formula_gravitational_force',
        'expression': 'F = G × m₁ × m₂ / r²',
        'unit': 'N',
        'params': [
            ('m1', 'mass', 'kg'),
            ('m2', 'mass', 'kg'),
            ('r', 'distance', 'm'),
        ],
        'compute': lambda values: Decimal('6.67430e-11') * values['m1'] * values['m2'] / values['r'] ** 2,
    },
    {
        'key': 'potential_energy',
        'label_key': 'formula_potential_energy',
        'expression': 'E = m × g × h',
        'unit': 'J',
        'params': [
            ('m', 'mass', 'kg'),
            ('h', 'height', 'm'),
        ],
        'compute': lambda values: values['m'] * Decimal('9.80665') * values['h'],
    },
    {
        'key': 'spring_energy',
        'label_key': 'formula_spring_energy',
        'expression': 'E = 0.5 × k × x²',
        'unit': 'J',
        'params': [
            ('k', 'spring_constant', 'N/m'),
            ('x', 'distance', 'm'),
        ],
        'compute': lambda values: Decimal('0.5') * values['k'] * values['x'] ** 2,
    },
    {
        'key': 'wave_energy',
        'label_key': 'formula_wave_energy',
        'expression': 'E = h × c / λ',
        'unit': 'J',
        'params': [
            ('lambda', 'wavelength', 'm'),
        ],
        'compute': lambda values: Decimal('6.62607015e-34') * Decimal('299792458') / values['lambda'],
    },
    {
        'key': 'work',
        'label_key': 'formula_work',
        'expression': 'W = F × d',
        'unit': 'J',
        'params': [
            ('F', 'force', 'N'),
            ('d', 'distance', 'm'),
        ],
        'compute': lambda values: values['F'] * values['d'],
    },
    {
        'key': 'heat_capacity',
        'label_key': 'formula_heat_capacity',
        'expression': 'Q = m × c × ΔT',
        'unit': 'J',
        'params': [
            ('m', 'mass', 'kg'),
            ('c', 'specific_heat_capacity', 'J/(kg·K)'),
            ('delta_T', 'temperature_change', 'K'),
        ],
        'compute': lambda values: values['m'] * values['c'] * values['delta_T'],
    },
    {
        'key': 'power',
        'label_key': 'formula_power',
        'expression': 'P = W / t',
        'unit': 'W',
        'params': [
            ('W', 'work', 'J'),
            ('t', 'time', 's'),
        ],
        'compute': lambda values: values['W'] / values['t'],
    },
    {
        'key': 'ph',
        'label_key': 'formula_ph',
        'expression': 'pH = -log10([H+])',
        'unit': '',
        'params': [
            ('H', 'hydrogen_ion_concentration', 'mol/L'),
        ],
        'compute': lambda values: -values['H'].log10(),
    },
    {
        'key': 'electrical_power',
        'label_key': 'formula_electrical_power',
        'expression': 'P = V × I',
        'unit': 'W',
        'params': [
            ('V', 'voltage', 'V'),
            ('I', 'current', 'A'),
        ],
        'compute': lambda values: values['V'] * values['I'],
    },
    {
        'key': 'electrical_energy',
        'label_key': 'formula_electrical_energy',
        'expression': 'E = P × t',
        'unit': 'J',
        'params': [
            ('P', 'power', 'W'),
            ('t', 'time', 's'),
        ],
        'compute': lambda values: values['P'] * values['t'],
    },
    {
        'key': 'joule_heat',
        'label_key': 'formula_joule_heat',
        'expression': 'Q = I² × R × t',
        'unit': 'J',
        'params': [
            ('I', 'current', 'A'),
            ('R', 'resistance', 'Ω'),
            ('t', 'time', 's'),
        ],
        'compute': lambda values: values['I'] ** 2 * values['R'] * values['t'],
    },
    {
        'key': 'coulombs_law',
        'label_key': 'formula_coulombs_law',
        'expression': 'F = k × q₁ × q₂ / r²',
        'unit': 'N',
        'params': [
            ('q1', 'charge_1', 'C'),
            ('q2', 'charge_2', 'C'),
            ('r', 'distance', 'm'),
        ],
        'compute': lambda values: Decimal('8.9875517923e9') * values['q1'] * values['q2'] / values['r'] ** 2,
    },
    {
        'key': 'electric_field',
        'label_key': 'formula_electric_field',
        'expression': 'E = F / q',
        'unit': 'V/m',
        'params': [
            ('F', 'force', 'N'),
            ('q', 'charge', 'C'),
        ],
        'compute': lambda values: values['F'] / values['q'],
    },
    {
        'key': 'capacitance',
        'label_key': 'formula_capacitance',
        'expression': 'C = Q / V',
        'unit': 'F',
        'params': [
            ('Q', 'charge', 'C'),
            ('V', 'voltage', 'V'),
        ],
        'compute': lambda values: values['Q'] / values['V'],
    },
    {
        'key': 'capacitor_energy',
        'label_key': 'formula_capacitor_energy',
        'expression': 'E = 0.5 × C × V²',
        'unit': 'J',
        'params': [
            ('C', 'capacitance', 'F'),
            ('V', 'voltage', 'V'),
        ],
        'compute': lambda values: Decimal('0.5') * values['C'] * values['V'] ** 2,
    },
    {
        'key': 'rc_time_constant',
        'label_key': 'formula_rc_time_constant',
        'expression': 'τ = R × C',
        'unit': 's',
        'params': [
            ('R', 'resistance', 'Ω'),
            ('C', 'capacitance', 'F'),
        ],
        'compute': lambda values: values['R'] * values['C'],
    },
    {
        'key': 'conductance',
        'label_key': 'formula_conductance',
        'expression': 'G = 1 / R',
        'unit': 'S',
        'params': [
            ('R', 'resistance', 'Ω'),
        ],
        'compute': lambda values: Decimal('1') / values['R'],
    },
    {
        'key': 'voltage_divider',
        'label_key': 'formula_voltage_divider',
        'expression': 'V_out = V_in × R₂ / (R₁ + R₂)',
        'unit': 'V',
        'params': [
            ('V_in', 'input_voltage', 'V'),
            ('R1', 'resistance_1', 'Ω'),
            ('R2', 'resistance_2', 'Ω'),
        ],
        'compute': lambda values: values['V_in'] * values['R2'] / (values['R1'] + values['R2']),
    },
    {
        'key': 'magnetic_force',
        'label_key': 'formula_magnetic_force',
        'expression': 'F = B × I × L',
        'unit': 'N',
        'params': [
            ('B', 'magnetic_field', 'T'),
            ('I', 'current', 'A'),
            ('L', 'length', 'm'),
        ],
        'compute': lambda values: values['B'] * values['I'] * values['L'],
    },
    {
        'key': 'inductance_energy',
        'label_key': 'formula_inductance_energy',
        'expression': 'E = 0.5 × L × I²',
        'unit': 'J',
        'params': [
            ('L', 'inductance', 'H'),
            ('I', 'current', 'A'),
        ],
        'compute': lambda values: Decimal('0.5') * values['L'] * values['I'] ** 2,
    },
    {
        'key': 'charge_flow',
        'label_key': 'formula_charge_flow',
        'expression': 'Q = I × t',
        'unit': 'C',
        'params': [
            ('I', 'current', 'A'),
            ('t', 'time', 's'),
        ],
        'compute': lambda values: values['I'] * values['t'],
    },
    {
        'key': 'power_dissipation',
        'label_key': 'formula_power_dissipation',
        'expression': 'P = I² × R',
        'unit': 'W',
        'params': [
            ('I', 'current', 'A'),
            ('R', 'resistance', 'Ω'),
        ],
        'compute': lambda values: values['I'] ** 2 * values['R'],
    },
    {
        'key': 'magnetic_field_wire',
        'label_key': 'formula_magnetic_field_wire',
        'expression': 'B = μ₀ × I / (2π × r)',
        'unit': 'T',
        'params': [
            ('I', 'current', 'A'),
            ('r', 'distance', 'm'),
        ],
        'compute': lambda values: (Decimal('1.25663706212e-6') * values['I']) / (Decimal('2') * Decimal('3.14159265358979') * values['r']),
    },
    {
        'key': 'newtons_second_law',
        'label_key': 'formula_newtons_second_law',
        'expression': 'F = m × a',
        'unit': 'N',
        'params': [
            ('m', 'mass', 'kg'),
            ('a', 'acceleration', 'm/s²'),
        ],
        'compute': lambda values: values['m'] * values['a'],
    },
    {
        'key': 'momentum',
        'label_key': 'formula_momentum',
        'expression': 'p = m × v',
        'unit': 'kg·m/s',
        'params': [
            ('m', 'mass', 'kg'),
            ('v', 'velocity', 'm/s'),
        ],
        'compute': lambda values: values['m'] * values['v'],
    },
    {
        'key': 'impulse',
        'label_key': 'formula_impulse',
        'expression': 'J = F × t',
        'unit': 'N·s',
        'params': [
            ('F', 'force', 'N'),
            ('t', 'time', 's'),
        ],
        'compute': lambda values: values['F'] * values['t'],
    },
    {
        'key': 'pressure',
        'label_key': 'formula_pressure',
        'expression': 'P = F / A',
        'unit': 'Pa',
        'params': [
            ('F', 'force', 'N'),
            ('A', 'area', 'm²'),
        ],
        'compute': lambda values: values['F'] / values['A'],
    },
    {
        'key': 'buoyant_force',
        'label_key': 'formula_buoyant_force',
        'expression': 'F = ρ × V × g',
        'unit': 'N',
        'params': [
            ('rho', 'density', 'kg/m³'),
            ('V', 'volume', 'm³'),
        ],
        'compute': lambda values: values['rho'] * values['V'] * Decimal('9.80665'),
    },
    {
        'key': 'wave_speed',
        'label_key': 'formula_wave_speed',
        'expression': 'v = λ × f',
        'unit': 'm/s',
        'params': [
            ('lambda', 'wavelength', 'm'),
            ('f', 'frequency', 'Hz'),
        ],
        'compute': lambda values: values['lambda'] * values['f'],
    },
    {
        'key': 'frequency_from_period',
        'label_key': 'formula_frequency_from_period',
        'expression': 'f = 1 / t',
        'unit': 'Hz',
        'params': [
            ('t', 'time', 's'),
        ],
        'compute': lambda values: Decimal('1') / values['t'],
    },
    {
        'key': 'impact_velocity',
        'label_key': 'formula_impact_velocity',
        'expression': 'v = √(2 × g × h)',
        'unit': 'm/s',
        'params': [
            ('h', 'height', 'm'),
        ],
        'compute': lambda values: Decimal(math.sqrt(2 * 9.80665 * float(values['h']))),
    },
    {
        'key': 'centripetal_force',
        'label_key': 'formula_centripetal_force',
        'expression': 'F = m × v² / r',
        'unit': 'N',
        'params': [
            ('m', 'mass', 'kg'),
            ('v', 'velocity', 'm/s'),
            ('r', 'distance', 'm'),
        ],
        'compute': lambda values: values['m'] * values['v'] ** 2 / values['r'],
    },
    {
        'key': 'power_force_velocity',
        'label_key': 'formula_force_velocity_power',
        'expression': 'P = F × v',
        'unit': 'W',
        'params': [
            ('F', 'force', 'N'),
            ('v', 'velocity', 'm/s'),
        ],
        'compute': lambda values: values['F'] * values['v'],
    },
    {
        'key': 'hydrostatic_pressure',
        'label_key': 'formula_hydrostatic_pressure',
        'expression': 'P = ρ × g × h',
        'unit': 'Pa',
        'params': [
            ('rho', 'density', 'kg/m³'),
            ('h', 'height', 'm'),
        ],
        'compute': lambda values: values['rho'] * Decimal('9.80665') * values['h'],
    },
    {
        'key': 'escape_velocity',
        'label_key': 'formula_escape_velocity',
        'expression': 'v = √(2 × G × M / r)',
        'unit': 'm/s',
        'params': [
            ('M', 'mass', 'kg'),
            ('r', 'distance', 'm'),
        ],
        'compute': lambda values: Decimal(math.sqrt(2 * 6.67430e-11 * float(values['M']) / float(values['r']))),
    },
    {
        'key': 'magnetic_flux',
        'label_key': 'formula_magnetic_flux',
        'expression': 'Φ = B × A',
        'unit': 'Wb',
        'params': [
            ('B', 'magnetic_field', 'T'),
            ('A', 'area', 'm²'),
        ],
        'compute': lambda values: values['B'] * values['A'],
    },
    {
        'key': 'parallel_plate_capacitance',
        'label_key': 'formula_parallel_plate_capacitance',
        'expression': 'C = ε₀ × A / d',
        'unit': 'F',
        'params': [
            ('A', 'area', 'm²'),
            ('d', 'distance', 'm'),
        ],
        'compute': lambda values: Decimal('8.8541878128e-12') * values['A'] / values['d'],
    },
    {
        'key': 'material_resistance',
        'label_key': 'formula_material_resistance',
        'expression': 'R = ρ × L / A',
        'unit': 'Ω',
        'params': [
            ('rho', 'resistivity', 'Ω·m'),
            ('L', 'distance', 'm'),
            ('A', 'area', 'm²'),
        ],
        'compute': lambda values: values['rho'] * values['L'] / values['A'],
    },
    {
        'key': 'stefan_boltzmann',
        'label_key': 'formula_stefan_boltzmann',
        'expression': 'P = σ × A × T⁴',
        'unit': 'W',
        'params': [
            ('A', 'area', 'm²'),
            ('T', 'temperature', 'K'),
        ],
        'compute': lambda values: Decimal('5.670374419e-8') * values['A'] * values['T'] ** 4,
    },
    {
        'key': 'de_broglie_wavelength',
        'label_key': 'formula_de_broglie_wavelength',
        'expression': 'λ = h / p',
        'unit': 'm',
        'params': [
            ('p', 'momentum', 'kg·m/s'),
        ],
        'compute': lambda values: Decimal('6.62607015e-34') / values['p'],
    },
    {
        'key': 'photon_energy',
        'label_key': 'formula_photon_energy',
        'expression': 'E = h × f',
        'unit': 'J',
        'params': [
            ('f', 'frequency', 'Hz'),
        ],
        'compute': lambda values: Decimal('6.62607015e-34') * values['f'],
    },
    {
        'key': 'kinetic_energy_momentum',
        'label_key': 'formula_kinetic_energy_momentum',
        'expression': 'E = p² / (2 × m)',
        'unit': 'J',
        'params': [
            ('p', 'momentum', 'kg·m/s'),
            ('m', 'mass', 'kg'),
        ],
        'compute': lambda values: values['p'] ** 2 / (Decimal('2') * values['m']),
    },
    {
        'key': 'lens_focal_length',
        'label_key': 'formula_lens_focal_length',
        'expression': 'f = d_o × d_i / (d_o + d_i)',
        'unit': 'm',
        'params': [
            ('d_o', 'object_distance', 'm'),
            ('d_i', 'image_distance', 'm'),
        ],
        'compute': lambda values: values['d_o'] * values['d_i'] / (values['d_o'] + values['d_i']),
    },
]


def parse_decimal(text: str) -> Decimal:
    text = text.strip().replace(',', '.')
    return Decimal(text) if text else Decimal('0')


def format_decimal(value: Decimal) -> str:
    quant = Decimal('1e-30')
    result = value.quantize(quant)
    return format(result, 'f')


class ExtendedModeDialog(QDialog):
    def __init__(self, parent=None, theme=None, get_text=None):
        super().__init__(parent)
        self.get_text = get_text or (lambda x: x)
        self.theme = theme or {}
        self.sort_ascending = True
        self.sorted_formulas = []
        self.search_query = ''
        self.setWindowTitle(self.get_text('extended_mode_title'))
        self.setMinimumSize(660, 460)
        self._build_ui()
        self._apply_theme()

    def _apply_theme(self):
        text = self.theme.get('TEXT_WHITE', '#eaeaf0')
        muted = self.theme.get('TEXT_MUTED', '#8888a0')
        panel = self.theme.get('PANEL_BG', '#22222a')
        display = self.theme.get('DISPLAY_BG', '#14141a')
        border = self.theme.get('BORDER', '#3a3a4a')
        hover = self.theme.get('CARD_HOVER', '#333340')
        self.setStyleSheet(f"""
            QDialog {{ background: {panel}; color: {text}; }}
            QLabel {{ color: {text}; }}
            QLineEdit, QTextEdit, QComboBox, QListWidget {{
                color: {text};
                background: {display};
                border: 1px solid {border};
                border-radius: 6px;
            }}
            QComboBox::drop-down {{ border-left: 1px solid {border}; }}
            QComboBox QAbstractItemView {{ background: {display}; color: {text}; selection-background-color: {hover}; }}
            QPushButton {{ color: {text}; background: {panel}; border: 1px solid {border}; border-radius: 6px; }}
            QPushButton:hover {{ background: {hover}; }}
            QListWidget {{ background: {display}; }}
        """)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(14, 14, 14, 14)

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)

        lbl_formula = QLabel(self.get_text('formula_select'))
        lbl_formula.setFont(QFont('Consolas', 11))
        header_layout.addWidget(lbl_formula)

        self.btn_sort = QPushButton(self.get_text('sort_az'))
        self.btn_sort.setFont(QFont('Consolas', 10))
        self.btn_sort.clicked.connect(self._toggle_sort)
        header_layout.addWidget(self.btn_sort)

        layout.addWidget(header)

        self.search_input = QLineEdit()
        self.search_input.setFont(QFont('Consolas', 11))
        self.search_input.setPlaceholderText(self.get_text('search_formulas'))
        self.search_input.textChanged.connect(self._filter_formulas)
        layout.addWidget(self.search_input)

        self.formula_list = QListWidget()
        self.formula_list.setFont(QFont('Consolas', 11))
        self.formula_list.currentRowChanged.connect(self._on_formula_row_changed)
        layout.addWidget(self.formula_list, stretch=1)

        self.scroll_slider = QSlider(Qt.Horizontal)
        self.scroll_slider.setMinimum(0)
        self.scroll_slider.setMaximum(0)
        self.scroll_slider.setSingleStep(1)
        self.scroll_slider.setPageStep(5)
        self.scroll_slider.valueChanged.connect(self._on_slider_changed)
        layout.addWidget(self.scroll_slider)

        self.expr_label = QLabel('')
        self.expr_label.setFont(QFont('Consolas', 11))
        self.expr_label.setStyleSheet('color: #c0c0c0;')
        layout.addWidget(self.expr_label)

        self.params_group = QGroupBox()
        self.params_group.setTitle(self.get_text('formula_expression'))
        self.params_group.setFont(QFont('Consolas', 10))
        self.params_form = QFormLayout(self.params_group)
        self.params_form.setLabelAlignment(Qt.AlignRight)
        self.params_form.setFormAlignment(Qt.AlignLeft)
        layout.addWidget(self.params_group)

        self.btn_compute = QPushButton(self.get_text('compute'))
        self.btn_compute.setFont(QFont('Consolas', 11))
        self.btn_compute.clicked.connect(self._compute_result)

        self.btn_pro_mode = QPushButton(self.get_text('pro_mode'))
        self.btn_pro_mode.setFont(QFont('Consolas', 11))
        self.btn_pro_mode.clicked.connect(self._open_pro_mode)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_compute)
        btn_layout.addWidget(self.btn_pro_mode)
        layout.addLayout(btn_layout)

        self.lbl_result = QLabel('')
        self.lbl_result.setFont(QFont('Consolas', 12, QFont.Bold))
        layout.addWidget(self.lbl_result)

        self.error_label = QLabel('')
        self.error_label.setFont(QFont('Consolas', 10))
        self.error_label.setStyleSheet('color: #ff8080;')
        layout.addWidget(self.error_label)

        self._populate_formula_list()
        self._refresh_formula()

    def _get_filtered_formulas(self):
        query = self.search_query.lower()
        filtered = [
            formula for formula in FORMULAS
            if query in self.get_text(formula['label_key']).lower()
            or query in formula['expression'].lower()
        ]
        return sorted(
            filtered,
            key=lambda formula: self.get_text(formula['label_key']),
            reverse=not self.sort_ascending,
        )

    def _populate_formula_list(self, selected_key=None):
        self.sorted_formulas = self._get_filtered_formulas()
        self.formula_list.blockSignals(True)
        self.formula_list.clear()

        for formula in self.sorted_formulas:
            self.formula_list.addItem(self.get_text(formula['label_key']))
            self.formula_list.item(self.formula_list.count() - 1).setToolTip(
                f"{formula['expression']}  [{formula.get('unit', '')}]"
            )

        self.scroll_slider.setMaximum(max(0, len(self.sorted_formulas) - 1))
        self.scroll_slider.setPageStep(max(1, len(self.sorted_formulas) // 5))

        selected_index = 0
        if selected_key is not None:
            selected_index = next(
                (index for index, formula in enumerate(self.sorted_formulas) if formula['key'] == selected_key),
                0,
            )

        if self.sorted_formulas:
            self.formula_list.setCurrentRow(selected_index)
            self._update_slider(selected_index)
        else:
            self.scroll_slider.setValue(0)

        self.formula_list.blockSignals(False)

    def _update_slider(self, index):
        self.scroll_slider.blockSignals(True)
        self.scroll_slider.setValue(index)
        self.scroll_slider.blockSignals(False)

    def _on_formula_row_changed(self, row):
        if row < 0 or row >= len(self.sorted_formulas):
            return
        self._update_slider(row)
        self._refresh_formula()

    def _on_slider_changed(self, value):
        if self.formula_list.currentRow() != value:
            self.formula_list.blockSignals(True)
            self.formula_list.setCurrentRow(value)
            self.formula_list.blockSignals(False)
        self._refresh_formula()

    def _filter_formulas(self):
        self.search_query = self.search_input.text().strip()
        self._populate_formula_list()

    def _toggle_sort(self):
        current_key = None
        current_row = self.formula_list.currentRow()
        if self.sorted_formulas and current_row >= 0:
            current_key = self.sorted_formulas[current_row]['key']
        self.sort_ascending = not self.sort_ascending
        self.btn_sort.setText(self.get_text('sort_az') if self.sort_ascending else self.get_text('sort_za'))
        self._populate_formula_list(selected_key=current_key)
        self._refresh_formula()

    def _refresh_formula(self) -> None:
        row = self.formula_list.currentRow()
        if row < 0 or row >= len(self.sorted_formulas):
            self.expr_label.setText('')
            while self.params_form.rowCount() > 0:
                self.params_form.removeRow(0)
            self.lbl_result.setText('')
            self.error_label.setText('')
            return

        formula = self.sorted_formulas[row]
        self.expr_label.setText(f"{self.get_text('formula_expression')}: {formula['expression']}")
        while self.params_form.rowCount() > 0:
            self.params_form.removeRow(0)
        self.param_inputs = {}

        for code, label_key, unit in formula['params']:
            input_widget = QLineEdit('0')
            input_widget.setFont(QFont('Consolas', 11))
            input_widget.setAlignment(Qt.AlignRight)
            input_widget.setPlaceholderText(unit or '0')
            self.param_inputs[code] = input_widget

            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(6)
            row_layout.addWidget(input_widget)
            row_layout.addWidget(QLabel(unit))
            self.params_form.addRow(f"{self.get_text(label_key)}:", row_widget)

        self.lbl_result.setText('')
        self.error_label.setText('')

    def _open_pro_mode(self):
        pro_dialog = ProModeDialog(self, self.theme, self.get_text)
        pro_dialog.exec_()

    def _compute_result(self) -> None:
        row = self.formula_list.currentRow()
        if row < 0 or row >= len(self.sorted_formulas):
            return
        formula = self.sorted_formulas[row]
        values = {}
        try:
            for code, _, _ in formula['params']:
                values[code] = parse_decimal(self.param_inputs[code].text())

            result = formula['compute'](values)
            formatted = format_decimal(result)
            unit = formula.get('unit', '')
            self.lbl_result.setText(f"{self.get_text('result')}: {formatted} {unit}")
            self.error_label.setText('')
        except (InvalidOperation, ZeroDivisionError) as exc:
            self.lbl_result.setText('')
            self.error_label.setText(str(exc))
        except Exception as exc:
            self.lbl_result.setText('')
            self.error_label.setText(self.get_text('error') + ': ' + str(exc))


class ProModeDialog(QDialog):
    def __init__(self, parent=None, theme=None, get_text=None):
        super().__init__(parent)
        self.get_text = get_text or (lambda x: x)
        self.theme = theme or {}
        self.advanced_mode = False
        self.advanced_fields = []
        self.setWindowTitle(self.get_text('pro_mode_title'))
        self.setMinimumSize(800, 650)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        chk_advanced = QCheckBox(self.get_text('advanced_mode'))
        chk_advanced.stateChanged.connect(self._toggle_advanced)
        layout.addWidget(chk_advanced)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_semiconductor_tab(), self.get_text('semiconductor_tab'))
        self.tabs.addTab(self._build_bit_calc_tab(), self.get_text('bit_calc_tab'))
        self.tabs.addTab(self._build_color_converter_tab(), self.get_text('color_tab'))
        self.tabs.addTab(self._build_base_converter_tab(), self.get_text('base_conv_tab'))
        self.tabs.addTab(self._build_developer_tab(), self.get_text('developer_tab'))
        self.tabs.addTab(self._build_hash_tab(), self.get_text('hash_tab'))
        self.tabs.addTab(self._build_graphing_tab(), self.get_text('graphing_tab'))
        self.tabs.addTab(self._build_matrix_tab(), self.get_text('matrix_tab'))
        self.tabs.addTab(self._build_equation_solver_tab(), self.get_text('equation_solver_tab'))
        self.tabs.addTab(self._build_statistics_tab(), self.get_text('statistics_tab'))
        self.tabs.addTab(self._build_complex_tab(), self.get_text('complex_tab'))
        layout.addWidget(self.tabs)

    def _toggle_advanced(self, state):
        self.advanced_mode = state == 2  # Qt.CheckState.Checked
        for field in self.advanced_fields:
            field.setVisible(self.advanced_mode)

    def _apply_theme(self, widget):
        text = self.theme.get('TEXT_WHITE', '#eaeaf0')
        muted = self.theme.get('TEXT_MUTED', '#8888a0')
        panel = self.theme.get('PANEL_BG', '#22222a')
        display = self.theme.get('DISPLAY_BG', '#14141a')
        border = self.theme.get('BORDER', '#3a3a4a')
        hover = self.theme.get('CARD_HOVER', '#333340')
        widget.setStyleSheet(f"""
            QWidget {{ background: {panel}; color: {text}; }}
            QLabel {{ color: {text}; }}
            QLineEdit, QTextEdit, QComboBox, QListWidget {{
                color: {text};
                background: {display};
                border: 1px solid {border};
                border-radius: 6px;
            }}
            QComboBox::drop-down {{ border-left: 1px solid {border}; }}
            QComboBox QAbstractItemView {{ background: {display}; color: {text}; selection-background-color: {hover}; }}
            QPushButton {{ color: {text}; background: {panel}; border: 1px solid {border}; border-radius: 6px; }}
            QPushButton:hover {{ background: {hover}; }}
            QListWidget {{ background: {display}; }}
        """)

    def _build_semiconductor_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel(self.get_text('semiconductor_title'))
        title.setFont(QFont('Consolas', 11, QFont.Bold))
        layout.addWidget(title)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignLeft)

        self.semi_usage_input = QLineEdit('1000')
        self.semi_usage_input.setFont(QFont('Consolas', 10))
        self.semi_usage_input.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('usage_time'), self.semi_usage_input)

        self.semi_current_input = QLineEdit('0.5')
        self.semi_current_input.setFont(QFont('Consolas', 10))
        self.semi_current_input.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('current_label'), self.semi_current_input)

        self.semi_tj_input = QLineEdit('85')
        self.semi_tj_input.setFont(QFont('Consolas', 10))
        self.semi_tj_input.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('junction_temp'), self.semi_tj_input)

        self.semi_ta_input = QLineEdit('25')
        self.semi_ta_input.setFont(QFont('Consolas', 10))
        self.semi_ta_input.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('ambient_temp'), self.semi_ta_input)

        self.semi_theta_input = QLineEdit('50')
        self.semi_theta_input.setFont(QFont('Consolas', 10))
        self.semi_theta_input.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('theta_ja'), self.semi_theta_input)

        self.semi_mtbf_input = QLineEdit('100000')
        self.semi_mtbf_input.setFont(QFont('Consolas', 10))
        self.semi_mtbf_input.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('mtbf_label'), self.semi_mtbf_input)

        self.semi_ea_input = QLineEdit('0.5')
        self.semi_ea_input.setFont(QFont('Consolas', 10))
        self.semi_ea_input.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('activation_energy'), self.semi_ea_input)

        # Advanced fields
        self.semi_voltage_input = QLineEdit('5')
        self.semi_voltage_input.setFont(QFont('Consolas', 10))
        self.semi_voltage_input.setAlignment(Qt.AlignRight)
        self.semi_voltage_input.setVisible(False)
        form.addRow(self.get_text('voltage_label'), self.semi_voltage_input)
        self.advanced_fields.append(self.semi_voltage_input)

        self.semi_power_input = QLineEdit('2.5')
        self.semi_power_input.setFont(QFont('Consolas', 10))
        self.semi_power_input.setAlignment(Qt.AlignRight)
        self.semi_power_input.setVisible(False)
        form.addRow(self.get_text('power_label'), self.semi_power_input)
        self.advanced_fields.append(self.semi_power_input)

        layout.addLayout(form)

        btn = QPushButton(self.get_text('compute'))
        btn.setFont(QFont('Consolas', 11))
        btn.clicked.connect(self._compute_semiconductor)
        layout.addWidget(btn)

        self.semi_result = QTextEdit()
        self.semi_result.setFont(QFont('Consolas', 9))
        self.semi_result.setReadOnly(True)
        self.semi_result.setMaximumHeight(200)
        layout.addWidget(self.semi_result)

        self.semi_error = QLabel('')
        self.semi_error.setFont(QFont('Consolas', 9))
        self.semi_error.setStyleSheet('color: #ff8080;')
        layout.addWidget(self.semi_error)
        layout.addStretch()

        return widget

    def _build_bit_calc_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel(self.get_text('bit_calc_title'))
        title.setFont(QFont('Consolas', 11, QFont.Bold))
        layout.addWidget(title)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignLeft)

        self.bit_input = QLineEdit('255')
        self.bit_input.setFont(QFont('Consolas', 10))
        self.bit_input.setAlignment(Qt.AlignRight)
        self.bit_input.textChanged.connect(self._update_bit_calc)
        form.addRow(self.get_text('decimal_label'), self.bit_input)

        self.bit_width_type = QComboBox()
        self.bit_width_type.addItems(['8', '16', '32', '64'])
        self.bit_width_type.currentIndexChanged.connect(self._update_bit_calc)
        form.addRow(self.get_text('bit_width_label'), self.bit_width_type)

        self.bit_signed_type = QComboBox()
        self.bit_signed_type.addItems([self.get_text('unsigned_option'), self.get_text('signed_option')])
        self.bit_signed_type.currentIndexChanged.connect(self._update_bit_calc)
        form.addRow(self.get_text('signed_mode_label'), self.bit_signed_type)

        self.bit_hex = QLineEdit()
        self.bit_hex.setFont(QFont('Consolas', 10))
        self.bit_hex.setReadOnly(True)
        self.bit_hex.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('hex_label'), self.bit_hex)

        self.bit_bin = QLineEdit()
        self.bit_bin.setFont(QFont('Consolas', 10))
        self.bit_bin.setReadOnly(True)
        self.bit_bin.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('binary_label'), self.bit_bin)

        self.bit_octal = QLineEdit()
        self.bit_octal.setFont(QFont('Consolas', 10))
        self.bit_octal.setReadOnly(True)
        self.bit_octal.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('octal_label'), self.bit_octal)

        self.bit_popcount = QLineEdit()
        self.bit_popcount.setFont(QFont('Consolas', 10))
        self.bit_popcount.setReadOnly(True)
        self.bit_popcount.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('bit_count'), self.bit_popcount)

        self.bit_signed_range = QLineEdit()
        self.bit_signed_range.setFont(QFont('Consolas', 10))
        self.bit_signed_range.setReadOnly(True)
        self.bit_signed_range.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('integer_range_label'), self.bit_signed_range)

        self.bit_twos_complement = QLineEdit()
        self.bit_twos_complement.setFont(QFont('Consolas', 10))
        self.bit_twos_complement.setReadOnly(True)
        self.bit_twos_complement.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('two_complement_label'), self.bit_twos_complement)

        self.bit_bytes = QLineEdit()
        self.bit_bytes.setFont(QFont('Consolas', 10))
        self.bit_bytes.setReadOnly(True)
        self.bit_bytes.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('byte_count_label'), self.bit_bytes)

        self.bit_msb = QLineEdit()
        self.bit_msb.setFont(QFont('Consolas', 10))
        self.bit_msb.setReadOnly(True)
        self.bit_msb.setAlignment(Qt.AlignRight)
        form.addRow(self.get_text('msb_pos'), self.bit_msb)

        layout.addLayout(form)
        layout.addStretch()
        self._update_bit_calc()

        return widget

    def _build_color_converter_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel(self.get_text('color_conv_title'))
        title.setFont(QFont('Consolas', 11, QFont.Bold))
        layout.addWidget(title)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignLeft)

        self.color_hex = QLineEdit('#FF0000')
        self.color_hex.setFont(QFont('Consolas', 10))
        self.color_hex.setAlignment(Qt.AlignRight)
        self.color_hex.textChanged.connect(self._update_color_conversion)
        form.addRow(self.get_text('hex_color'), self.color_hex)

        self.color_rgb = QLineEdit()
        self.color_rgb.setFont(QFont('Consolas', 10))
        self.color_rgb.setReadOnly(True)
        form.addRow(self.get_text('rgb_color'), self.color_rgb)

        self.color_hsl = QLineEdit()
        self.color_hsl.setFont(QFont('Consolas', 10))
        self.color_hsl.setReadOnly(True)
        form.addRow(self.get_text('hsl_color'), self.color_hsl)

        self.color_preview = QLineEdit()
        self.color_preview.setFont(QFont('Consolas', 10))
        self.color_preview.setReadOnly(True)
        self.color_preview.setMinimumHeight(40)
        form.addRow(self.get_text('color_preview'), self.color_preview)

        layout.addLayout(form)
        layout.addStretch()
        self._update_color_conversion()

        return widget

    def _build_base_converter_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel(self.get_text('base_conv_title'))
        title.setFont(QFont('Consolas', 11, QFont.Bold))
        layout.addWidget(title)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignLeft)

        self.base_input_type = QComboBox()
        self.base_input_type.addItems([
            self.get_text('decimal_label'),
            self.get_text('binary_label'),
            self.get_text('octal_label'),
            self.get_text('hex_label')
        ])
        self.base_input_type.currentIndexChanged.connect(self._update_base_conversion)
        form.addRow(self.get_text('input_base'), self.base_input_type)

        self.base_input = QLineEdit('255')
        self.base_input.setFont(QFont('Consolas', 10))
        self.base_input.setAlignment(Qt.AlignRight)
        self.base_input.textChanged.connect(self._update_base_conversion)
        form.addRow(self.get_text('input_label'), self.base_input)

        self.base_decimal = QLineEdit()
        self.base_decimal.setFont(QFont('Consolas', 10))
        self.base_decimal.setReadOnly(True)
        form.addRow(self.get_text('decimal_output'), self.base_decimal)

        self.base_binary = QLineEdit()
        self.base_binary.setFont(QFont('Consolas', 10))
        self.base_binary.setReadOnly(True)
        form.addRow(self.get_text('binary_output'), self.base_binary)

        self.base_octal = QLineEdit()
        self.base_octal.setFont(QFont('Consolas', 10))
        self.base_octal.setReadOnly(True)
        form.addRow(self.get_text('octal_output'), self.base_octal)

        self.base_hex = QLineEdit()
        self.base_hex.setFont(QFont('Consolas', 10))
        self.base_hex.setReadOnly(True)
        form.addRow(self.get_text('hex_output'), self.base_hex)

        layout.addLayout(form)
        layout.addStretch()
        self._update_base_conversion()

        return widget

    def _build_developer_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel(self.get_text('developer_tools_title'))
        title.setFont(QFont('Consolas', 11, QFont.Bold))
        layout.addWidget(title)

        int_group = QGroupBox(self.get_text('integer_conversion_title'))
        int_group.setFont(QFont('Consolas', 10))
        int_layout = QFormLayout(int_group)
        int_layout.setLabelAlignment(Qt.AlignRight)
        int_layout.setFormAlignment(Qt.AlignLeft)

        self.dev_int_input = QLineEdit('42')
        self.dev_int_input.setFont(QFont('Consolas', 10))
        self.dev_int_input.setAlignment(Qt.AlignRight)
        self.dev_int_input.textChanged.connect(self._update_dev_tools)
        int_layout.addRow(self.get_text('integer_input_label'), self.dev_int_input)

        self.dev_int_base = QComboBox()
        self.dev_int_base.addItems([
            self.get_text('decimal_label'),
            self.get_text('hex_label'),
            self.get_text('binary_label'),
            self.get_text('octal_label'),
        ])
        self.dev_int_base.currentIndexChanged.connect(self._update_dev_tools)
        int_layout.addRow(self.get_text('integer_base_label'), self.dev_int_base)

        self.dev_int_width = QComboBox()
        self.dev_int_width.addItems(['8', '16', '32', '64'])
        self.dev_int_width.currentIndexChanged.connect(self._update_dev_tools)
        int_layout.addRow(self.get_text('integer_width_label'), self.dev_int_width)

        self.dev_int_signed = QComboBox()
        self.dev_int_signed.addItems([self.get_text('unsigned_option'), self.get_text('signed_option')])
        self.dev_int_signed.currentIndexChanged.connect(self._update_dev_tools)
        int_layout.addRow(self.get_text('signed_mode_label'), self.dev_int_signed)

        self.dev_int_range = QLineEdit()
        self.dev_int_range.setFont(QFont('Consolas', 10))
        self.dev_int_range.setReadOnly(True)
        self.dev_int_range.setAlignment(Qt.AlignRight)
        int_layout.addRow(self.get_text('integer_range_label'), self.dev_int_range)

        self.dev_int_twos = QLineEdit()
        self.dev_int_twos.setFont(QFont('Consolas', 10))
        self.dev_int_twos.setReadOnly(True)
        self.dev_int_twos.setAlignment(Qt.AlignRight)
        int_layout.addRow(self.get_text('two_complement_label'), self.dev_int_twos)

        self.dev_int_bytes = QLineEdit()
        self.dev_int_bytes.setFont(QFont('Consolas', 10))
        self.dev_int_bytes.setReadOnly(True)
        self.dev_int_bytes.setAlignment(Qt.AlignRight)
        int_layout.addRow(self.get_text('byte_count_label'), self.dev_int_bytes)

        layout.addWidget(int_group)

        epoch_group = QGroupBox(self.get_text('timestamp_title'))
        epoch_group.setFont(QFont('Consolas', 10))
        epoch_layout = QFormLayout(epoch_group)
        epoch_layout.setLabelAlignment(Qt.AlignRight)
        epoch_layout.setFormAlignment(Qt.AlignLeft)

        self.dev_epoch_input = QLineEdit('1700000000')
        self.dev_epoch_input.setFont(QFont('Consolas', 10))
        self.dev_epoch_input.setAlignment(Qt.AlignRight)
        self.dev_epoch_input.textChanged.connect(self._update_dev_tools)
        epoch_layout.addRow(self.get_text('epoch_input_label'), self.dev_epoch_input)

        self.dev_datetime_input = QLineEdit('2025-01-01 00:00:00')
        self.dev_datetime_input.setFont(QFont('Consolas', 10))
        self.dev_datetime_input.setAlignment(Qt.AlignRight)
        self.dev_datetime_input.textChanged.connect(self._update_dev_tools)
        epoch_layout.addRow(self.get_text('datetime_input_label'), self.dev_datetime_input)

        self.dev_epoch_seconds = QLineEdit()
        self.dev_epoch_seconds.setFont(QFont('Consolas', 10))
        self.dev_epoch_seconds.setReadOnly(True)
        self.dev_epoch_seconds.setAlignment(Qt.AlignRight)
        epoch_layout.addRow(self.get_text('epoch_seconds_label'), self.dev_epoch_seconds)

        self.dev_epoch_ms = QLineEdit()
        self.dev_epoch_ms.setFont(QFont('Consolas', 10))
        self.dev_epoch_ms.setReadOnly(True)
        self.dev_epoch_ms.setAlignment(Qt.AlignRight)
        epoch_layout.addRow(self.get_text('epoch_milliseconds_label'), self.dev_epoch_ms)

        self.dev_datetime_output = QLineEdit()
        self.dev_datetime_output.setFont(QFont('Consolas', 10))
        self.dev_datetime_output.setReadOnly(True)
        self.dev_datetime_output.setAlignment(Qt.AlignRight)
        epoch_layout.addRow(self.get_text('iso_datetime_label'), self.dev_datetime_output)

        layout.addWidget(epoch_group)
        layout.addStretch()
        self._update_dev_tools()

        return widget

    def _build_hash_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel(self.get_text('hash_title'))
        title.setFont(QFont('Consolas', 11, QFont.Bold))
        layout.addWidget(title)

        lbl_input = QLabel(self.get_text('input_text'))
        lbl_input.setFont(QFont('Consolas', 10))
        layout.addWidget(lbl_input)

        self.hash_input = QTextEdit()
        self.hash_input.setFont(QFont('Consolas', 10))
        self.hash_input.setMaximumHeight(80)
        self.hash_input.textChanged.connect(self._update_hashes)
        layout.addWidget(self.hash_input)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignLeft)

        self.hash_md5 = QLineEdit()
        self.hash_md5.setFont(QFont('Consolas', 8))
        self.hash_md5.setReadOnly(True)
        form.addRow(self.get_text('md5_label'), self.hash_md5)

        self.hash_sha1 = QLineEdit()
        self.hash_sha1.setFont(QFont('Consolas', 8))
        self.hash_sha1.setReadOnly(True)
        form.addRow(self.get_text('sha1_label'), self.hash_sha1)

        self.hash_sha256 = QLineEdit()
        self.hash_sha256.setFont(QFont('Consolas', 8))
        self.hash_sha256.setReadOnly(True)
        form.addRow(self.get_text('sha256_label'), self.hash_sha256)

        self.hash_crc32 = QLineEdit()
        self.hash_crc32.setFont(QFont('Consolas', 8))
        self.hash_crc32.setReadOnly(True)
        form.addRow(self.get_text('crc32_label'), self.hash_crc32)

        self.hash_base64 = QLineEdit()
        self.hash_base64.setFont(QFont('Consolas', 8))
        self.hash_base64.setReadOnly(True)
        form.addRow(self.get_text('base64_label'), self.hash_base64)

        layout.addLayout(form)
        layout.addStretch()

        return widget

    def _compute_semiconductor(self):
        try:
            usage_time = float(self.semi_usage_input.text() or '0')
            current = float(self.semi_current_input.text() or '0')
            tj = float(self.semi_tj_input.text() or '85')
            ta = float(self.semi_ta_input.text() or '25')
            theta = float(self.semi_theta_input.text() or '50')
            mtbf_ref = float(self.semi_mtbf_input.text() or '100000')
            ea = float(self.semi_ea_input.text() or '0.5')

            if current <= 0 or mtbf_ref <= 0:
                raise ValueError("Current and MTBF must be positive")

            # Arrhenius equation: λ(T) = λ₀ × exp(Ea / k × (1/T₁ - 1/T₂))
            # k = Boltzmann constant = 8.617e-5 eV/K
            k_boltzmann = 8.617e-5
            t_ref = 25 + 273.15  # Reference temperature in Kelvin
            t_junction = tj + 273.15  # Junction temperature in Kelvin

            # Temperature acceleration factor
            temp_factor = math.exp((ea / k_boltzmann) * (1 / t_ref - 1 / t_junction))

            # Current acceleration factor (power law)
            current_factor = current ** 1.5 if current > 0.1 else current

            # Combined model: λ = λ_ref × (I/I_ref)^n × exp(temp_factor)
            failure_rate = (mtbf_ref ** -1) * current_factor * temp_factor
            lifetime = 1 / failure_rate if failure_rate > 0 else float('inf')
            remaining = max(0, lifetime - usage_time)
            reliability = math.exp(-failure_rate * usage_time)

            result_text = f"Lifetime (Arrhenius): {lifetime:.2f} hours\n"
            result_text += f"Remaining life: {remaining:.2f} hours\n"
            result_text += f"Reliability @ {usage_time:.0f}h: {reliability*100:.4f}%\n"
            result_text += f"Failure rate: {failure_rate*1e6:.6f} /hour\n"
            result_text += f"Temperature factor: {temp_factor:.6f}x\n"
            result_text += f"Current factor: {current_factor:.6f}x"

            self.semi_result.setText(result_text)
            self.semi_error.setText('')
        except ValueError as e:
            self.semi_result.setText('')
            self.semi_error.setText(str(e))
        except Exception as e:
            self.semi_result.setText('')
            self.semi_error.setText(f"Error: {str(e)}")

    def _update_bit_calc(self):
        try:
            value = int(self.bit_input.text() or '0')
            width = int(self.bit_width_type.currentText())
            signed = self.bit_signed_type.currentText() == self.get_text('signed_option')
            mask = (1 << width) - 1
            self.bit_hex.setText(f"0x{value & mask:X}")
            self.bit_bin.setText(f"0b{value & mask:b}")
            self.bit_octal.setText(f"0o{value & mask:o}")
            self.bit_popcount.setText(str(bin(value & mask).count('1')))
            self.bit_msb.setText(str((value & mask).bit_length() - 1) if value != 0 else '0')

            if signed:
                min_val = -(1 << (width - 1))
                max_val = (1 << (width - 1)) - 1
                self.bit_signed_range.setText(f"{min_val}..{max_val}")
                self.bit_twos_complement.setText(f"0x{value & mask:X}")
            else:
                min_val = 0
                max_val = mask
                self.bit_signed_range.setText(f"{min_val}..{max_val}")
                self.bit_twos_complement.setText(f"0x{value & mask:X}")

            self.bit_bytes.setText(f"{width // 8} {self.get_text('bytes_label')}")
        except ValueError:
            self.bit_hex.setText('')
            self.bit_bin.setText('')
            self.bit_octal.setText('')
            self.bit_popcount.setText('')
            self.bit_signed_range.setText('')
            self.bit_twos_complement.setText('')
            self.bit_bytes.setText('')
            self.bit_msb.setText('')

    def _update_dev_tools(self):
        def parse_int_value(text, base):
            if not text:
                return 0
            return int(text.strip(), base)

        try:
            base_index = self.dev_int_base.currentIndex()
            bases = [10, 16, 2, 8]
            value = parse_int_value(self.dev_int_input.text(), bases[base_index])
            width = int(self.dev_int_width.currentText())
            signed = self.dev_int_signed.currentText() == self.get_text('signed_option')
            mask = (1 << width) - 1
            if signed:
                min_val = -(1 << (width - 1))
                max_val = (1 << (width - 1)) - 1
                signed_value = value if min_val <= value <= max_val else value - (1 << width)
                self.dev_int_range.setText(f"{min_val}..{max_val}")
                self.dev_int_twos.setText(f"0x{value & mask:X}")
            else:
                min_val = 0
                max_val = mask
                self.dev_int_range.setText(f"{min_val}..{max_val}")
                self.dev_int_twos.setText(f"0x{value & mask:X}")
            self.dev_int_bytes.setText(f"{width // 8} {self.get_text('bytes_label')}")
        except ValueError:
            self.dev_int_range.setText('')
            self.dev_int_twos.setText('')
            self.dev_int_bytes.setText('')

        try:
            text = self.dev_epoch_input.text().strip()
            if text.isdigit():
                seconds = int(text)
                self.dev_epoch_seconds.setText(str(seconds))
                self.dev_epoch_ms.setText(str(seconds * 1000))
                self.dev_datetime_output.setText(datetime.datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S UTC'))
            else:
                self.dev_epoch_seconds.setText('')
                self.dev_epoch_ms.setText('')
                self.dev_datetime_output.setText('')
        except Exception:
            self.dev_epoch_seconds.setText('')
            self.dev_epoch_ms.setText('')
            self.dev_datetime_output.setText('')

        try:
            dt_text = self.dev_datetime_input.text().strip()
            dt_value = datetime.datetime.strptime(dt_text, '%Y-%m-%d %H:%M:%S')
            timestamp = int(dt_value.replace(tzinfo=datetime.timezone.utc).timestamp())
            self.dev_epoch_seconds.setText(str(timestamp))
            self.dev_epoch_ms.setText(str(timestamp * 1000))
            self.dev_datetime_output.setText(dt_value.strftime('%Y-%m-%d %H:%M:%S UTC'))
        except Exception:
            pass

    def _update_color_conversion(self):
        try:
            hex_val = self.color_hex.text().strip()
            if not hex_val.startswith('#'):
                hex_val = '#' + hex_val
            hex_val = hex_val.lstrip('#')
            if len(hex_val) == 6:
                r = int(hex_val[0:2], 16)
                g = int(hex_val[2:4], 16)
                b = int(hex_val[4:6], 16)
                self.color_rgb.setText(f"rgb({r}, {g}, {b})")

                # RGB to HSL conversion
                r_norm, g_norm, b_norm = r / 255, g / 255, b / 255
                max_c = max(r_norm, g_norm, b_norm)
                min_c = min(r_norm, g_norm, b_norm)
                l = (max_c + min_c) / 2
                if max_c == min_c:
                    h = s = 0
                else:
                    d = max_c - min_c
                    s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
                    if max_c == r_norm:
                        h = 60 * (((g_norm - b_norm) / d + (6 if g_norm < b_norm else 0)) % 6)
                    elif max_c == g_norm:
                        h = 60 * (((b_norm - r_norm) / d + 2) % 6)
                    else:
                        h = 60 * (((r_norm - g_norm) / d + 4) % 6)
                self.color_hsl.setText(f"hsl({h:.1f}°, {s*100:.1f}%, {l*100:.1f}%)")
                self.color_preview.setStyleSheet(f"background-color: #{hex_val};")
        except (ValueError, IndexError):
            self.color_rgb.setText('')
            self.color_hsl.setText('')

    def _update_base_conversion(self):
        try:
            bases = [10, 2, 8, 16]
            input_base = bases[self.base_input_type.currentIndex()]
            input_val = self.base_input.text().strip()
            if input_base == 2 and input_val.startswith('0b'):
                input_val = input_val[2:]
            elif input_base == 8 and input_val.startswith('0o'):
                input_val = input_val[2:]
            elif input_base == 16 and input_val.startswith('0x'):
                input_val = input_val[2:]
            value = int(input_val, input_base)
            self.base_decimal.setText(str(value))
            self.base_binary.setText(f"0b{value:b}")
            self.base_octal.setText(f"0o{value:o}")
            self.base_hex.setText(f"0x{value:X}")
        except ValueError:
            self.base_decimal.setText('')
            self.base_binary.setText('')
            self.base_octal.setText('')
            self.base_hex.setText('')

    def _update_hashes(self):
        text = self.hash_input.toPlainText()
        data = text.encode('utf-8')
        self.hash_md5.setText(hashlib.md5(data).hexdigest())
        self.hash_sha1.setText(hashlib.sha1(data).hexdigest())
        self.hash_sha256.setText(hashlib.sha256(data).hexdigest())
        self.hash_crc32.setText(format(binascii.crc32(data) & 0xFFFFFFFF, '08x'))
        self.hash_base64.setText(base64.b64encode(data).decode('ascii'))

    def _build_graphing_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel('Graphing Calculator')
        title.setFont(QFont('Consolas', 11, QFont.Bold))
        layout.addWidget(title)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignLeft)

        self.graph_function_input = QLineEdit('x**2')
        self.graph_function_input.setFont(QFont('Consolas', 10))
        form.addRow(self.get_text('function_label'), self.graph_function_input)

        range_layout = QHBoxLayout()
        range_layout.addWidget(QLabel(self.get_text('x_range_label')))
        self.graph_x_from = QLineEdit('-10')
        self.graph_x_from.setFont(QFont('Consolas', 10))
        self.graph_x_from.setFixedWidth(80)
        range_layout.addWidget(QLabel(self.get_text('from_label')))
        range_layout.addWidget(self.graph_x_from)
        self.graph_x_to = QLineEdit('10')
        self.graph_x_to.setFont(QFont('Consolas', 10))
        self.graph_x_to.setFixedWidth(80)
        range_layout.addWidget(QLabel(self.get_text('to_label')))
        range_layout.addWidget(self.graph_x_to)
        range_layout.addStretch()
        form.addRow(range_layout)

        plot_button = QPushButton(self.get_text('plot_button'))
        plot_button.clicked.connect(self._plot_graph)
        form.addRow(plot_button)

        layout.addLayout(form)

        self.graph_canvas = FigureCanvas(Figure(figsize=(5, 4), dpi=100))
        layout.addWidget(self.graph_canvas)

        self._apply_theme(widget)
        return widget

    def _plot_graph(self):
        try:
            func_str = self.graph_function_input.text()
            x_from = float(self.graph_x_from.text())
            x_to = float(self.graph_x_to.text())
            # Simple linspace replacement
            num_points = 1000
            x = [x_from + i * (x_to - x_from) / (num_points - 1) for i in range(num_points)]
            safe_dict = {"sin": math.sin, "cos": math.cos, "tan": math.tan, "exp": math.exp, "log": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e}
            y = [eval(func_str, {"__builtins__": None}, {"x": xi, **safe_dict}) for xi in x]
            self.graph_canvas.figure.clear()
            ax = self.graph_canvas.figure.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.grid(True)
            self.graph_canvas.draw()
        except Exception as e:
            self.graph_canvas.figure.clear()
            ax = self.graph_canvas.figure.add_subplot(111)
            ax.text(0.5, 0.5, f'Error: {str(e)}', ha='center', va='center', transform=ax.transAxes)
            self.graph_canvas.draw()

    def _build_matrix_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel('Matrix Calculator')
        title.setFont(QFont('Consolas', 11, QFont.Bold))
        layout.addWidget(title)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignLeft)

        self.matrix_a_input = QTextEdit('1 2\n3 4')
        self.matrix_a_input.setFont(QFont('Consolas', 10))
        self.matrix_a_input.setMaximumHeight(80)
        form.addRow(self.get_text('matrix_a_label'), self.matrix_a_input)

        self.matrix_b_input = QTextEdit('5 6\n7 8')
        self.matrix_b_input.setFont(QFont('Consolas', 10))
        self.matrix_b_input.setMaximumHeight(80)
        form.addRow(self.get_text('matrix_b_label'), self.matrix_b_input)

        buttons_layout = QHBoxLayout()
        add_button = QPushButton(self.get_text('add_button'))
        add_button.clicked.connect(self._matrix_add)
        buttons_layout.addWidget(add_button)

        multiply_button = QPushButton(self.get_text('multiply_button'))
        multiply_button.clicked.connect(self._matrix_multiply)
        buttons_layout.addWidget(multiply_button)

        det_button = QPushButton(self.get_text('determinant_button'))
        det_button.clicked.connect(self._matrix_determinant)
        buttons_layout.addWidget(det_button)

        form.addRow(buttons_layout)

        self.matrix_result = QTextEdit()
        self.matrix_result.setFont(QFont('Consolas', 10))
        self.matrix_result.setReadOnly(True)
        form.addRow(self.get_text('result_label'), self.matrix_result)

        layout.addLayout(form)

        self._apply_theme(widget)
        return widget

    def _matrix_add(self):
        try:
            a = self._parse_matrix(self.matrix_a_input.toPlainText())
            b = self._parse_matrix(self.matrix_b_input.toPlainText())
            result = self._add_matrices(a, b)
            self.matrix_result.setPlainText('\n'.join(' '.join(f'{x:.2f}' for x in row) for row in result))
        except Exception as e:
            self.matrix_result.setPlainText(f'Error: {str(e)}')

    def _matrix_multiply(self):
        try:
            a = self._parse_matrix(self.matrix_a_input.toPlainText())
            b = self._parse_matrix(self.matrix_b_input.toPlainText())
            result = self._multiply_matrices(a, b)
            self.matrix_result.setPlainText('\n'.join(' '.join(f'{x:.2f}' for x in row) for row in result))
        except Exception as e:
            self.matrix_result.setPlainText(f'Error: {str(e)}')

    def _matrix_determinant(self):
        try:
            a = self._parse_matrix(self.matrix_a_input.toPlainText())
            det = self._determinant(a)
            self.matrix_result.setPlainText(f'Determinant: {det:.2f}')
        except Exception as e:
            self.matrix_result.setPlainText(f'Error: {str(e)}')

    def _parse_matrix(self, text):
        lines = text.strip().split('\n')
        matrix = []
        for line in lines:
            row = [float(x) for x in line.split()]
            matrix.append(row)
        return matrix

    def _add_matrices(self, a, b):
        if len(a) != len(b) or len(a[0]) != len(b[0]):
            raise ValueError("Matrices must have the same dimensions")
        return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

    def _multiply_matrices(self, a, b):
        if len(a[0]) != len(b):
            raise ValueError("Number of columns in A must equal number of rows in B")
        result = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]
        for i in range(len(a)):
            for j in range(len(b[0])):
                for k in range(len(b)):
                    result[i][j] += a[i][k] * b[k][j]
        return result

    def _determinant(self, matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        if n == 3:
            return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) -
                    matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
                    matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))
        raise ValueError("Determinant only for 1x1, 2x2, 3x3 matrices")

    def _build_equation_solver_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel('Equation Solver')
        title.setFont(QFont('Consolas', 11, QFont.Bold))
        layout.addWidget(title)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignLeft)

        self.eq_input = QTextEdit('2*x + 3*y = 5\n4*x + y = 6')
        self.eq_input.setFont(QFont('Consolas', 10))
        self.eq_input.setMaximumHeight(100)
        form.addRow(self.get_text('equations_label'), self.eq_input)

        solve_button = QPushButton(self.get_text('solve_button'))
        solve_button.clicked.connect(self._solve_equations)
        form.addRow(solve_button)

        self.eq_result = QTextEdit()
        self.eq_result.setFont(QFont('Consolas', 10))
        self.eq_result.setReadOnly(True)
        form.addRow(self.get_text('variables_label'), self.eq_result)

        layout.addLayout(form)

        self._apply_theme(widget)
        return widget

    def _solve_equations(self):
        try:
            lines = self.eq_input.toPlainText().strip().split('\n')
            if len(lines) != 2:
                raise ValueError("Only 2 equations supported")
            coeffs = []
            constants = []
            for line in lines:
                if '=' in line:
                    left, right = line.split('=')
                    eq = left.strip().replace(' ', '')
                    c = float(right.strip())
                    # Simple: assume 2*x + 3*y
                    parts = eq.replace('+', ' +').replace('-', ' -').split()
                    a = b = 0
                    for part in parts:
                        if part.endswith('*x'):
                            a = float(part[:-2])
                        elif part.endswith('*y'):
                            b = float(part[:-2])
                        elif part == 'x':
                            a = 1
                        elif part == 'y':
                            b = 1
                        elif part == '-x':
                            a = -1
                        elif part == '-y':
                            b = -1
                    coeffs.append([a, b])
                    constants.append(c)
            # Solve 2x2
            a1, b1 = coeffs[0]
            a2, b2 = coeffs[1]
            c1, c2 = constants
            det = a1 * b2 - a2 * b1
            if det == 0:
                raise ValueError("No unique solution")
            x = (c1 * b2 - c2 * b1) / det
            y = (a1 * c2 - a2 * c1) / det
            self.eq_result.setPlainText(f'x = {x:.2f}, y = {y:.2f}')
        except Exception as e:
            self.eq_result.setPlainText(f'Error: {str(e)}')

    def _build_statistics_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel('Statistics Calculator')
        title.setFont(QFont('Consolas', 11, QFont.Bold))
        layout.addWidget(title)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignLeft)

        self.stat_data_input = QTextEdit('1 2 3 4 5')
        self.stat_data_input.setFont(QFont('Consolas', 10))
        self.stat_data_input.setMaximumHeight(80)
        form.addRow(self.get_text('data_label'), self.stat_data_input)

        buttons_layout = QHBoxLayout()
        mean_button = QPushButton(self.get_text('mean_button'))
        mean_button.clicked.connect(self._stat_mean)
        buttons_layout.addWidget(mean_button)

        std_button = QPushButton(self.get_text('std_button'))
        std_button.clicked.connect(self._stat_std)
        buttons_layout.addWidget(std_button)

        reg_button = QPushButton(self.get_text('regression_button'))
        reg_button.clicked.connect(self._stat_regression)
        buttons_layout.addWidget(reg_button)

        # Advanced buttons
        median_button = QPushButton(self.get_text('median_button'))
        median_button.clicked.connect(self._stat_median)
        median_button.setVisible(False)
        buttons_layout.addWidget(median_button)
        self.advanced_fields.append(median_button)

        mode_button = QPushButton(self.get_text('mode_button'))
        mode_button.clicked.connect(self._stat_mode)
        mode_button.setVisible(False)
        buttons_layout.addWidget(mode_button)
        self.advanced_fields.append(mode_button)

        form.addRow(buttons_layout)

        self.stat_result = QTextEdit()
        self.stat_result.setFont(QFont('Consolas', 10))
        self.stat_result.setReadOnly(True)
        form.addRow(self.get_text('result_label'), self.stat_result)

        layout.addLayout(form)

        self._apply_theme(widget)
        return widget

    def _stat_mean(self):
        try:
            data = [float(x) for x in self.stat_data_input.toPlainText().split()]
            mean = statistics.mean(data)
            self.stat_result.setPlainText(f'Mean: {mean:.2f}')
        except Exception as e:
            self.stat_result.setPlainText(f'Error: {str(e)}')

    def _stat_std(self):
        try:
            data = [float(x) for x in self.stat_data_input.toPlainText().split()]
            std = statistics.stdev(data)
            self.stat_result.setPlainText(f'Std Dev: {std:.2f}')
        except Exception as e:
            self.stat_result.setPlainText(f'Error: {str(e)}')

    def _stat_regression(self):
        try:
            data = [float(x) for x in self.stat_data_input.toPlainText().split()]
            x = list(range(len(data)))
            mean_x = statistics.mean(x)
            mean_y = statistics.mean(data)
            numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, data))
            denominator = sum((xi - mean_x) ** 2 for xi in x)
            slope = numerator / denominator
            intercept = mean_y - slope * mean_x
            ss_res = sum((yi - (slope * xi + intercept)) ** 2 for xi, yi in zip(x, data))
            ss_tot = sum((yi - mean_y) ** 2 for yi in data)
            r_squared = 1 - (ss_res / ss_tot)
            self.stat_result.setPlainText(f'Slope: {slope:.2f}, Intercept: {intercept:.2f}, R²: {r_squared:.2f}')
        except Exception as e:
            self.stat_result.setPlainText(f'Error: {str(e)}')

    def _stat_median(self):
        try:
            data = [float(x) for x in self.stat_data_input.toPlainText().split()]
            data.sort()
            n = len(data)
            if n % 2 == 1:
                median = data[n // 2]
            else:
                median = (data[n // 2 - 1] + data[n // 2]) / 2
            self.stat_result.setPlainText(f'Median: {median:.2f}')
        except Exception as e:
            self.stat_result.setPlainText(f'Error: {str(e)}')

    def _stat_mode(self):
        try:
            data = [float(x) for x in self.stat_data_input.toPlainText().split()]
            freq = {}
            for num in data:
                freq[num] = freq.get(num, 0) + 1
            mode = max(freq, key=freq.get)
            self.stat_result.setPlainText(f'Mode: {mode:.2f}')
        except Exception as e:
            self.stat_result.setPlainText(f'Error: {str(e)}')

    def _build_complex_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel('Complex Number Calculator')
        title.setFont(QFont('Consolas', 11, QFont.Bold))
        layout.addWidget(title)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignLeft)

        self.complex_a_input = QLineEdit('1+2j')
        self.complex_a_input.setFont(QFont('Consolas', 10))
        form.addRow(self.get_text('complex_a_label'), self.complex_a_input)

        self.complex_b_input = QLineEdit('3-4j')
        self.complex_b_input.setFont(QFont('Consolas', 10))
        form.addRow(self.get_text('complex_b_label'), self.complex_b_input)

        self.complex_op_combo = QComboBox()
        self.complex_op_combo.addItems([self.get_text('add_op'), self.get_text('sub_op'), self.get_text('mul_op'), self.get_text('div_op'), self.get_text('conjugate_op'), self.get_text('abs_op')])
        form.addRow(self.get_text('complex_op_label'), self.complex_op_combo)

        calc_button = QPushButton(self.get_text('calculate_button'))
        calc_button.clicked.connect(self._complex_calculate)
        form.addRow(calc_button)

        self.complex_result = QLineEdit()
        self.complex_result.setFont(QFont('Consolas', 10))
        self.complex_result.setReadOnly(True)
        form.addRow(self.get_text('result_label'), self.complex_result)

        layout.addLayout(form)

        self._apply_theme(widget)
        return widget

    def _complex_calculate(self):
        try:
            a = complex(self.complex_a_input.text())
            op = self.complex_op_combo.currentText()
            if op in [self.get_text('conjugate_op'), self.get_text('abs_op')]:
                if op == self.get_text('conjugate_op'):
                    result = a.conjugate()
                elif op == self.get_text('abs_op'):
                    result = abs(a)
            else:
                b = complex(self.complex_b_input.text())
                if op == self.get_text('add_op'):
                    result = a + b
                elif op == self.get_text('sub_op'):
                    result = a - b
                elif op == self.get_text('mul_op'):
                    result = a * b
                elif op == self.get_text('div_op'):
                    result = a / b
            self.complex_result.setText(str(result))
        except Exception as e:
            self.complex_result.setText(f'Error: {str(e)}')
