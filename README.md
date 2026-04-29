```markdown
# Calculator (School Project)

A simple calculator built with Python and PyQt5. Made as a school project.

## Requirements

- Python 3.7+
- PyQt5 >= 5.15.0
- matplotlib >= 3.5.0

## Installation

1. Make sure Python 3.x is installed
2. Install the dependencies:

```bash
pip install PyQt5>=5.15.0 matplotlib>=3.5.0
```

3. Run the program:

```bash
python main.py
```

## Project Structure

```
main.py                    # Entry point
engineering_calculator.py  # Core calculator logic
extended_mode.py           # Extended mode
units_converter.py         # Units converter
README.md                  # Documentation
```

## Usage

After launching, a calculator window will open. Enter numbers and operations using the buttons or your keyboard.

## Interface Language

The calculator supports three languages. Set the `CALC_LANG` environment variable before running to choose a language:

```bash
# Ukrainian (default)
export CALC_LANG=uk
python main.py

# Russian
export CALC_LANG=ru
python main.py

# English
export CALC_LANG=en
python main.py
```
```