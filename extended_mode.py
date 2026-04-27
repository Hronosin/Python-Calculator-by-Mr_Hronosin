"""Extended Mode for high-precision scientific and chemical calculations."""

from decimal import Decimal, InvalidOperation, getcontext
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLabel,
    QLineEdit, QPushButton, QWidget, QFormLayout, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import math

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

        self.formula_combo = QComboBox()
        self.formula_combo.setFont(QFont('Consolas', 11))
        self.formula_combo.addItems([self.get_text(formula['label_key']) for formula in FORMULAS])
        self.formula_combo.currentIndexChanged.connect(self._refresh_formula)
        header_layout.addWidget(self.formula_combo, stretch=1)

        layout.addWidget(header)

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

        self.lbl_note = QLabel(self.get_text('precision_note'))
        self.lbl_note.setFont(QFont('Consolas', 9))
        self.lbl_note.setStyleSheet('color: #88bbee;')
        layout.addWidget(self.lbl_note)

        self.error_label = QLabel('')
        self.error_label.setFont(QFont('Consolas', 10))
        self.error_label.setStyleSheet('color: #ff8080;')
        layout.addWidget(self.error_label)

        self._refresh_formula()

    def _refresh_formula(self) -> None:
        formula = FORMULAS[self.formula_combo.currentIndex()]
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
        formula = FORMULAS[self.formula_combo.currentIndex()]
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
        self.setMinimumSize(500, 400)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel(self.get_text('semiconductor_lifetime'))
        title.setFont(QFont('Consolas', 14, QFont.Bold))
        layout.addWidget(title)

        self.params_form = QFormLayout()
        self.params_form.setLabelAlignment(Qt.AlignRight)
        self.params_form.setFormAlignment(Qt.AlignLeft)

        self.usage_time_input = QLineEdit('0')
        self.usage_time_input.setFont(QFont('Consolas', 11))
        self.usage_time_input.setAlignment(Qt.AlignRight)
        self.params_form.addRow(self.get_text('usage_time') + ':', self.usage_time_input)

        self.current_input = QLineEdit('0')
        self.current_input.setFont(QFont('Consolas', 11))
        self.current_input.setAlignment(Qt.AlignRight)
        self.params_form.addRow(self.get_text('current') + ':', self.current_input)

        self.min_temp_input = QLineEdit('0')
        self.min_temp_input.setFont(QFont('Consolas', 11))
        self.min_temp_input.setAlignment(Qt.AlignRight)
        self.params_form.addRow(self.get_text('min_temp') + ':', self.min_temp_input)

        self.max_temp_input = QLineEdit('0')
        self.max_temp_input.setFont(QFont('Consolas', 11))
        self.max_temp_input.setAlignment(Qt.AlignRight)
        self.params_form.addRow(self.get_text('max_temp') + ':', self.max_temp_input)

        self.avg_temp_input = QLineEdit('25')
        self.avg_temp_input.setFont(QFont('Consolas', 11))
        self.avg_temp_input.setAlignment(Qt.AlignRight)
        self.params_form.addRow(self.get_text('avg_temp') + ':', self.avg_temp_input)

        layout.addLayout(self.params_form)

        self.btn_compute = QPushButton(self.get_text('compute'))
        self.btn_compute.setFont(QFont('Consolas', 11))
        self.btn_compute.clicked.connect(self._compute_lifetime)
        layout.addWidget(self.btn_compute)

        self.lbl_lifetime = QLabel('')
        self.lbl_lifetime.setFont(QFont('Consolas', 12, QFont.Bold))
        layout.addWidget(self.lbl_lifetime)

        self.lbl_remaining = QLabel('')
        self.lbl_remaining.setFont(QFont('Consolas', 12))
        layout.addWidget(self.lbl_remaining)

        self.error_label = QLabel('')
        self.error_label.setFont(QFont('Consolas', 10))
        self.error_label.setStyleSheet('color: #ff8080;')
        layout.addWidget(self.error_label)

    def _compute_lifetime(self):
        try:
            usage_time = float(self.usage_time_input.text() or '0')
            current = float(self.current_input.text() or '0')
            min_temp = float(self.min_temp_input.text() or '0')
            max_temp = float(self.max_temp_input.text() or '0')
            avg_temp = float(self.avg_temp_input.text() or '25')

            if current <= 0:
                raise ValueError("Current must be positive")

            # Simplified model: lifetime = base * exp(temp_factor) / current^1.5
            # Base lifetime at 25°C and 1A
            base_lifetime = 100000  # hours
            temp_factor = 0.01 * (100 - avg_temp)  # higher temp reduces lifetime
            current_factor = current ** 1.5

            lifetime = base_lifetime * math.exp(temp_factor) / current_factor
            remaining = lifetime - usage_time

            self.lbl_lifetime.setText(f"{self.get_text('lifetime_result')}: {lifetime:.2f}")
            self.lbl_remaining.setText(f"{self.get_text('remaining_lifetime')}: {max(0, remaining):.2f}")
            self.error_label.setText('')
        except ValueError as e:
            self.lbl_lifetime.setText('')
            self.lbl_remaining.setText('')
            self.error_label.setText(str(e))
        except Exception as e:
            self.lbl_lifetime.setText('')
            self.lbl_remaining.setText('')
            self.error_label.setText(self.get_text('error') + ': ' + str(e))
