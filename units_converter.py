"""
Units converter for the engineering calculator
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QComboBox, QLabel,
    QLineEdit, QTabWidget, QWidget, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class UnitsConverter(QDialog):
    """Dialog for converting units"""
    
    def __init__(self, parent=None, theme=None, get_text=None):
        super().__init__(parent)
        self.theme = theme or {}
        self.get_text = get_text or (lambda x: x)
        self.setWindowTitle(self.get_text("units_title"))
        self.setMinimumSize(500, 400)
        self.setup_ui()
        
    def setup_ui(self):
        """Creates the interface"""
        layout = QVBoxLayout(self)
        
        # Tabs for different conversion types
        tabs = QTabWidget()
        
        tabs.addTab(self.create_distance_tab(), "📏 " + self.get_text('distance'))
        tabs.addTab(self.create_weight_tab(), "⚖️ " + self.get_text('weight'))
        tabs.addTab(self.create_temp_tab(), "🌡️ " + self.get_text('temperature'))
        tabs.addTab(self.create_time_tab(), "⏱️ " + self.get_text('time'))
        tabs.addTab(self.create_volume_tab(), "🧃 " + self.get_text('volume'))
        tabs.addTab(self.create_area_tab(), "📐 " + self.get_text('area'))
        tabs.addTab(self.create_speed_tab(), "⚡ " + self.get_text('speed'))
        tabs.addTab(self.create_energy_tab(), "⚡ " + self.get_text('energy'))
        tabs.addTab(self.create_pressure_tab(), "📊 " + self.get_text('pressure'))
        tabs.addTab(self.create_force_tab(), "💪 " + self.get_text('force'))
        
        layout.addWidget(tabs)
        
    def create_converter_tab(self, conversions):
        """Creates a converter tab"""
        widget = QWidget()
        layout = QGridLayout(widget)
        
        layout.addWidget(QLabel(self.get_text('from')), 0, 0)
        from_unit = QComboBox()
        from_unit.addItems(conversions.keys())
        layout.addWidget(from_unit, 0, 1)
        
        from_value = QLineEdit("1")
        layout.addWidget(from_value, 0, 2)
        
        layout.addWidget(QLabel("→"), 1, 1)
        
        layout.addWidget(QLabel(self.get_text('to')), 2, 0)
        to_unit = QComboBox()
        layout.addWidget(to_unit, 2, 1)
        
        to_value = QLineEdit("1")
        to_value.setReadOnly(True)
        layout.addWidget(to_value, 2, 2)
        
        def do_convert():
            try:
                val = float(from_value.text())
                from_u = from_unit.currentText()
                to_u = to_unit.currentText()
                
                if from_u in conversions and to_u in conversions[from_u]:
                    result = val * conversions[from_u][to_u]
                    to_value.setText(f"{result:.10g}")
                else:
                    to_value.setText("N/A")
            except:
                to_value.setText("Error")
        
        def update_to_units(text):
            to_unit.clear()
            if text in conversions:
                to_unit.addItems(conversions[text].keys())
            do_convert()
        
        from_unit.currentTextChanged.connect(update_to_units)
        from_value.textChanged.connect(do_convert)
        to_unit.currentTextChanged.connect(do_convert)
        
        update_to_units(from_unit.currentText())
        layout.setRowStretch(3, 1)
        return widget
    
    def create_distance_tab(self):
        conversions = {
            "m": {"km": 0.001, "cm": 100, "mm": 1000, "μm": 1000000, "nm": 1e9, "in": 39.3701, "ft": 3.28084, "yd": 1.09361, "mi": 0.000621371, "nmi": 0.000539957},
            "km": {"m": 1000, "cm": 100000, "mm": 1000000, "in": 39370.1, "ft": 3280.84, "yd": 1093.61, "mi": 0.621371, "nmi": 0.539957},
            "cm": {"m": 0.01, "km": 0.00001, "mm": 10, "in": 0.393701, "ft": 0.0328084, "yd": 0.0109361},
            "mm": {"m": 0.001, "km": 0.000001, "cm": 0.1, "μm": 1000, "in": 0.0393701, "ft": 0.00328084},
            "μm": {"m": 0.000001, "mm": 0.001, "nm": 1000},
            "nm": {"m": 1e-9, "μm": 0.001},
            "in": {"m": 0.0254, "cm": 2.54, "mm": 25.4, "ft": 0.083333, "yd": 0.027778},
            "ft": {"m": 0.3048, "cm": 30.48, "mm": 304.8, "in": 12, "yd": 0.333333, "mi": 0.000189394},
            "yd": {"m": 0.9144, "ft": 3, "mi": 0.000568182},
            "mi": {"m": 1609.34, "km": 1.60934, "ft": 5280, "yd": 1760, "nmi": 0.868976},
            "nmi": {"m": 1852, "km": 1.852, "mi": 1.15078},
        }
        return self.create_converter_tab(conversions)
    
    def create_weight_tab(self):
        conversions = {
            "kg": {"g": 1000, "mg": 1000000, "μg": 1e9, "lb": 2.20462, "oz": 35.274, "st": 0.157473, "t": 0.001},
            "g": {"kg": 0.001, "mg": 1000, "μg": 1000000, "lb": 0.00220462, "oz": 0.035274},
            "mg": {"kg": 0.000001, "g": 0.001, "μg": 1000},
            "μg": {"mg": 0.001},
            "lb": {"kg": 0.453592, "g": 453.592, "oz": 16, "st": 0.071429},
            "oz": {"kg": 0.0283495, "g": 28.3495, "lb": 0.0625},
            "st": {"kg": 6.35029, "lb": 14},
            "t": {"kg": 1000},
        }
        return self.create_converter_tab(conversions)
    
    def create_temp_tab(self):
        widget = QWidget()
        layout = QGridLayout(widget)
        
        layout.addWidget(QLabel(self.get_text('from')), 0, 0)
        from_unit = QComboBox()
        from_unit.addItems(["°C", "°F", "K"])
        layout.addWidget(from_unit, 0, 1)
        
        from_value = QLineEdit("0")
        layout.addWidget(from_value, 0, 2)
        
        layout.addWidget(QLabel("→"), 1, 1)
        layout.addWidget(QLabel(self.get_text('to')), 2, 0)
        to_unit = QComboBox()
        to_unit.addItems(["°C", "°F", "K"])
        layout.addWidget(to_unit, 2, 1)
        
        to_value = QLineEdit("0")
        to_value.setReadOnly(True)
        layout.addWidget(to_value, 2, 2)
        
        def convert_temp():
            try:
                val = float(from_value.text())
                from_u = from_unit.currentText()
                to_u = to_unit.currentText()
                
                if from_u == "°C":
                    c = val
                elif from_u == "°F":
                    c = (val - 32) * 5/9
                else:
                    c = val - 273.15
                
                if to_u == "°C":
                    result = c
                elif to_u == "°F":
                    result = c * 9/5 + 32
                else:
                    result = c + 273.15
                
                to_value.setText(f"{result:.10g}")
            except:
                to_value.setText("Error")
        
        from_value.textChanged.connect(convert_temp)
        from_unit.currentTextChanged.connect(convert_temp)
        to_unit.currentTextChanged.connect(convert_temp)
        
        convert_temp()
        layout.setRowStretch(3, 1)
        return widget
    
    def create_time_tab(self):
        conversions = {
            "s": {"ms": 1000, "μs": 1e6, "ns": 1e9, "min": 1/60, "h": 1/3600, "d": 1/86400, "w": 1/604800, "y": 1/31536000},
            "ms": {"s": 0.001, "μs": 1000, "min": 1/60000},
            "μs": {"ms": 0.001, "ns": 1000},
            "ns": {"μs": 0.001},
            "min": {"s": 60, "h": 1/60, "d": 1/1440},
            "h": {"s": 3600, "min": 60, "d": 1/24},
            "d": {"s": 86400, "min": 1440, "h": 24, "w": 1/7},
            "w": {"d": 7},
            "y": {"d": 365},
        }
        return self.create_converter_tab(conversions)
    
    def create_volume_tab(self):
        conversions = {
            "L": {"mL": 1000, "μL": 1e6, "m³": 0.001, "cm³": 1000, "in³": 61.0237, "gal": 0.264172, "pt": 2.11338, "fl oz": 33.814},
            "mL": {"L": 0.001, "μL": 1000, "cm³": 1, "in³": 0.0610237},
            "μL": {"mL": 0.001},
            "m³": {"L": 1000, "km³": 0.000000001},
            "cm³": {"mL": 1, "in³": 0.0610237},
            "in³": {"cm³": 16.3871, "L": 0.0163871},
            "gal": {"L": 3.78541, "pt": 8, "fl oz": 128},
            "pt": {"L": 0.473176, "gal": 0.125},
            "fl oz": {"mL": 29.5735, "L": 0.0295735},
        }
        return self.create_converter_tab(conversions)
    
    def create_area_tab(self):
        conversions = {
            "m²": {"km²": 0.000001, "cm²": 10000, "mm²": 1e6, "in²": 1550, "ft²": 10.7639, "yd²": 1.19599, "acre": 0.000247105, "ha": 0.0001},
            "km²": {"m²": 1000000, "mi²": 0.386102, "acre": 247.105},
            "cm²": {"m²": 0.0001, "mm²": 100},
            "mm²": {"cm²": 0.01},
            "in²": {"cm²": 6.4516, "ft²": 0.00694444},
            "ft²": {"m²": 0.092903, "in²": 144, "yd²": 0.111111},
            "yd²": {"ft²": 9, "m²": 0.836127},
            "acre": {"m²": 4046.86, "km²": 0.00404686, "mi²": 0.0015625},
            "ha": {"m²": 10000, "acre": 2.47105},
        }
        return self.create_converter_tab(conversions)
    
    def create_speed_tab(self):
        conversions = {
            "m/s": {"km/h": 3.6, "mph": 2.23694, "kt": 1.94384, "ft/s": 3.28084},
            "km/h": {"m/s": 0.277778, "mph": 0.621371, "kt": 0.539957},
            "mph": {"m/s": 0.44704, "km/h": 1.60934, "kt": 0.868976},
            "kt": {"m/s": 0.51444, "km/h": 1.852, "mph": 1.15078},
            "ft/s": {"m/s": 0.3048},
        }
        return self.create_converter_tab(conversions)
    
    def create_energy_tab(self):
        conversions = {
            "J": {"kJ": 0.001, "MJ": 0.000001, "cal": 0.239006, "kcal": 0.000239006, "Wh": 0.000277778, "kWh": 0.000000277778, "eV": 6.242e18, "BTU": 0.000947817},
            "kJ": {"J": 1000, "cal": 239.006},
            "cal": {"J": 4.184, "kcal": 0.001, "BTU": 0.00396567},
            "kcal": {"J": 4184, "cal": 1000},
            "Wh": {"J": 3600, "kWh": 0.001},
            "kWh": {"J": 3600000, "Wh": 1000},
            "eV": {"J": 1.602e-19},
            "BTU": {"J": 1055.06, "cal": 252.164},
        }
        return self.create_converter_tab(conversions)
    
    def create_pressure_tab(self):
        conversions = {
            "Pa": {"kPa": 0.001, "bar": 0.00001, "atm": 0.00000986923, "mmHg": 0.00750062, "psi": 0.000145038, "hPa": 0.01},
            "kPa": {"Pa": 1000, "bar": 0.01, "atm": 0.00986923, "mmHg": 7.50062, "psi": 0.145038},
            "bar": {"Pa": 100000, "kPa": 100, "atm": 0.986923, "psi": 14.5038},
            "atm": {"Pa": 101325, "kPa": 101.325, "bar": 1.01325, "mmHg": 760},
            "mmHg": {"Pa": 133.322, "kPa": 0.133322, "atm": 0.00131579},
            "psi": {"Pa": 6894.76, "kPa": 6.89476, "bar": 0.0689476, "atm": 0.068046},
            "hPa": {"Pa": 100, "kPa": 0.1},
        }
        return self.create_converter_tab(conversions)
    
    def create_force_tab(self):
        conversions = {
            "N": {"kN": 0.001, "dyn": 100000, "kgf": 0.101972, "lbf": 0.224809, "pdl": 7.23301},
            "kN": {"N": 1000},
            "dyn": {"N": 0.00001},
            "kgf": {"N": 9.80665, "lbf": 2.20462},
            "lbf": {"N": 4.44822, "kgf": 0.453592},
            "pdl": {"N": 0.138255},
        }
        return self.create_converter_tab(conversions)
