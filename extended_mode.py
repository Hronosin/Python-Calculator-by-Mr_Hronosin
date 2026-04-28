"""Extended Mode for high-precision scientific and chemical calculations."""

from decimal import Decimal, InvalidOperation, getcontext
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QWidget, QFormLayout, QGroupBox, QSlider, QListWidget, QTabWidget,
    QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import math
import hashlib

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
            input_widget.setPlaceholderText('0')
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
        self.setWindowTitle(self.get_text('pro_mode_title'))
        self.setMinimumSize(800, 650)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_semiconductor_tab(), self.get_text('semiconductor_tab'))
        self.tabs.addTab(self._build_bit_calc_tab(), self.get_text('bit_calc_tab'))
        self.tabs.addTab(self._build_color_converter_tab(), self.get_text('color_tab'))
        self.tabs.addTab(self._build_base_converter_tab(), self.get_text('base_conv_tab'))
        self.tabs.addTab(self._build_hash_tab(), self.get_text('hash_tab'))
        layout.addWidget(self.tabs)

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
            self.bit_hex.setText(f"0x{value:X}")
            self.bit_bin.setText(f"0b{value:b}")
            self.bit_octal.setText(f"0o{value:o}")
            self.bit_popcount.setText(str(bin(value).count('1')))
            self.bit_msb.setText(str(value.bit_length() - 1) if value > 0 else '0')
        except ValueError:
            self.bit_hex.setText('')
            self.bit_bin.setText('')
            self.bit_octal.setText('')
            self.bit_popcount.setText('')
            self.bit_msb.setText('')

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
