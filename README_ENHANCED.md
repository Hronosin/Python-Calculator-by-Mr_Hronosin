# 🧮 Engineering Calculator — Enhanced 2.0

![Design](https://img.shields.io/badge/Design-Minimalist%20Space-00d9ff?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776ab?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**Multi-language calculator with advanced mathematical functions, plotting, and a minimalist cosmic UI**

---

## 🌟 Quick Start

```bash
python main.py
```

The calculator opens with a beautiful cosmic-themed dark interface.

---

## 🎨 Features Showcase

### 🌌 Minimalist Cosmic Design
- **Dark theme** with neon accents (Cyan, Purple, Pink, Green)
- **Responsive layout** with input field and history panel
- **Status bar** with real-time feedback
- **Smooth animations** and color transitions

### ⌨️ Full Text Editing
- **Edit anywhere** in the expression field
- **Delete** removes character before cursor position
- **Ctrl+A** selects all text
- No need to retype entire expression when fixing a mistake

### 🧬 Advanced Math Functions
| Category | Functions |
|----------|-----------|
| **Trigonometric** | sin, cos, tan, asin, acos, atan |
| **Hyperbolic** | sinh, cosh, tanh |
| **Exponential** | exp, log, ln, log10 |
| **Other** | sqrt, root, factorial, abs |
| **Complex** | Support for `i` or `2+3j` format |
| **Constants** | pi, e |

### 📊 Function Plotting
- **Plot** button generates graphs for expressions with variable `x`
- Dynamic scaling and axis visualization
- Examples: `sin(x)`, `x^2-2*x+1`, `1/x`

### 🎓 Calculus Tools
- **d/dx** — Numerical derivative at point
- **∫** — Numerical definite integral
- Supports custom bounds

### 🔄 Unit Conversions
```
km_to_m(5)       → 5000
mi_to_km(1)      → 1.609344
c_to_f(0)        → 32
deg_to_rad(180)  → 3.14159...
```

### 📱 Supported Languages
- 🇬🇧 English
- 🇺🇦 Українська
- 🇷🇺 Русский

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Enter** | Calculate expression |
| **Esc** | Clear field |
| **Delete/Backspace** | Remove character before cursor |
| **Ctrl+A** | Select all text |
| **Ctrl+C** | Copy result to clipboard |
| **Ctrl+O** | Import history from JSON |
| **Ctrl+E** | Export history to JSON |
| **Ctrl+H** | Clear history |

---

## 📋 Usage Examples

### Basic Calculations
```
2 + 2 * 3              → 8
10 / 2 - 3             → 2
2 ^ 10                 → 1024 (powers)
sqrt(16)               → 4
factorial(5)           → 120
```

### Trigonometry
```
sin(pi/2)              → 1.0
cos(pi)                → -1.0
tan(pi/4)              → 1.0
rad_to_deg(pi)         → 180
```

### Complex Numbers
```
2 + 3j                 → (2+3j)
sqrt(-1)               → 1j
i * i                  → -1 (i is sqrt(-1))
```

### Exponential & Logarithms
```
exp(1)                 → 2.718... (e)
log(100)               → 4.605... (natural log)
log10(100)             → 2.0
root(8, 3)             → 2.0 (cube root)
```

### Unit Conversions
```
c_to_f(100)            → 212 (Celsius to Fahrenheit)
km_to_m(1.5)           → 1500
deg_to_rad(45)         → 0.7854... (degrees to radians)
```

### Calculus
- Click **d/dx** → enter x value → get derivative
- Click **∫** → enter bounds like "0, 5" → get integral

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- tkinter (usually included with Python)

### Setup
```bash
# Clone repository
git clone https://github.com/Hronosin/Python-Calculator-by-Mr_Hronosin.git
cd Python-Calculator-by-Mr_Hronosin

# Run directly
python main.py
```

---

## 📁 Project Structure

```
.
├── main.py                 # Application entry point
├── ui.py                   # GUI with cosmic design
├── calculator_core.py      # Math engine & functions
├── history_manager.py      # History import/export
├── dialogs.py              # Custom dialogs
├── engineering_calculator.py  # Legacy code
└── README_ENHANCED.md      # This file
```

---

## 🎯 Key Improvements v2.0

✨ **Cosmic Minimalist Design**
- Dark theme with neon accents
- Cleaner, more modern UI
- Improved visual hierarchy

✨ **Better Text Editing**
- Edit anywhere in expression
- Smart deletion with cursor position awareness
- Full keyboard support

✨ **Enhanced UX**
- Real-time status bar feedback
- Compact controls
- Intuitive button layout

✨ **New Functions**
- Advanced trigonometry (inverse, hyperbolic)
- Unit conversions
- Calculus tools (derivatives, integrals)
- Complex number support

✨ **Internationalization**
- Full support for 3 languages
- Dynamic language switching
- Localized all UI elements

---

## 🐛 Known Limitations

- Plotting uses tkinter Canvas (basic functionality)
- Numerical methods approximate derivatives/integrals
- Complex number support limited to specific operations

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 📄 License

MIT License — Feel free to use, modify, and distribute

---

## 👨‍💻 Author

**Mr_Hronosin**  
Enhanced Version 2.0 — April 2026

---

## 🚀 Future Roadmap

- [ ] Matrix operations
- [ ] Statistical functions
- [ ] Programmable variables
- [ ] Custom function definitions
- [ ] Better plotting (matplotlib integration)
- [ ] Hardware acceleration
- [ ] Mobile app version

---

**Enjoy your calculations! 🌟**
