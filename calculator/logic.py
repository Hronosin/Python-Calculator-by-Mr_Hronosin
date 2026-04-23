"""
Calculation logic for the engineering calculator.
"""

import math
import json
import os
from .config import HISTORY_FILE, STATE_FILE

class CalculatorLogic:
    """Handles all calculation operations."""

    def __init__(self):
        self.expr = ""
        self.last_res = None
        self.memory = 0.0
        self.angle_mode = "DEG"  # DEG / RAD
        self.inv_mode = False
        self.just_calc = False
        self.history = []
        self.load_history()
        self.load_state()

    def _to_rad(self, x):
        return x * math.pi / 180 if self.angle_mode == "DEG" else x

    def _from_rad(self, x):
        return x * 180 / math.pi if self.angle_mode == "DEG" else x

    FN_MAP = {
        "sin":   lambda self, x: math.sin(self._to_rad(x)) if not self.inv_mode else self._from_rad(math.asin(x)),
        "cos":   lambda self, x: math.cos(self._to_rad(x)) if not self.inv_mode else self._from_rad(math.acos(x)),
        "tan":   lambda self, x: math.tan(self._to_rad(x)) if not self.inv_mode else self._from_rad(math.atan(x)),
        "sinh":  lambda self, x: math.sinh(x)  if not self.inv_mode else math.asinh(x),
        "cosh":  lambda self, x: math.cosh(x)  if not self.inv_mode else math.acosh(x),
        "tanh":  lambda self, x: math.tanh(x)  if not self.inv_mode else math.atanh(x),
        "log":   lambda self, x: math.log10(x) if not self.inv_mode else 10**x,
        "ln":    lambda self, x: math.log(x)   if not self.inv_mode else math.exp(x),
        "log2":  lambda self, x: math.log2(x),
        "exp":   lambda self, x: math.exp(x),
        "sqrt":  lambda self, x: math.sqrt(x),
        "cbrt":  lambda self, x: x ** (1/3) if x >= 0 else -((-x) ** (1/3)),
        "pow2":  lambda self, x: x ** 2,
        "pow10": lambda self, x: 10 ** x,
        "abs":   lambda self, x: abs(x),
        "inv":   lambda self, x: 1 / x,
        "pct":   lambda self, x: x / 100,
        "floor": lambda self, x: math.floor(x),
        "ceil":  lambda self, x: math.ceil(x),
        "round": lambda self, x: round(x),
        "fact":  lambda self, x: float(math.factorial(int(x))),
    }

    CONST_MAP = {
        "PI":  math.pi,
        "E":   math.e,
        "PHI": (1 + math.sqrt(5)) / 2,
    }

    def _fmt(self, n):
        if not math.isfinite(n):
            return str(n)
        if abs(n) > 1e12 or (0 < abs(n) < 1e-7):
            return f"{n:.6e}"
        r = round(n, 12)
        s = f"{r:.12f}".rstrip("0").rstrip(".")
        return s

    def input_num(self, d):
        if self.just_calc:
            self.expr = ""; self.just_calc = False
        self.expr += d
        return self.expr

    def input_dot(self):
        if self.just_calc:
            self.expr = "0"; self.just_calc = False
        parts = self.expr.replace("**", " ").replace("*", " ").replace("/", " ") \
                         .replace("+", " ").replace("-", " ").split()
        last = parts[-1] if parts else ""
        if "." not in last:
            self.expr += "."
            return self.expr
        return self.expr

    def input_str(self, s):
        if self.just_calc and s in "+-*/%(":
            pass  # допустимо продолжить с результатом
        elif self.just_calc:
            self.just_calc = False
        self.expr += s
        return self.expr

    def input_const(self, c):
        if self.just_calc:
            self.expr = ""; self.just_calc = False
        self.expr += str(self.CONST_MAP[c])[:12]
        return self.expr

    def toggle_sign(self):
        if not self.expr:
            return self.expr
        if self.expr.startswith("-"):
            self.expr = self.expr[1:]
        else:
            self.expr = "-" + self.expr
        return self.expr

    def input_fn(self, fn):
        """Добавляет функцию в выражение как текст"""
        if self.just_calc:
            self.expr = ""; self.just_calc = False
        self.expr += f"{fn}("
        return self.expr

    def input_fn(self, fn):
        """Добавляет функцию в выражение как текст"""
        if self.just_calc:
            self.expr = ""; self.just_calc = False
        self.expr += f"{fn}("
        return self.expr

    def apply_fn(self, fn):
        """Применяет функцию к последнему числу (для старых кнопок)"""
        if not self.expr and self.last_res is not None:
            self.expr = self._fmt(self.last_res)
        if not self.expr:
            return None, None
        try:
            val = float(eval(self.expr, {"__builtins__": {}}, {}))
            f = self.FN_MAP[fn]
            res = f(self, val)
            label = f"{fn}({self._fmt(val)})"
            self._add_history(label, res)
            self.last_res = res
            self.expr = self._fmt(res)
            self.just_calc = True
            return self._fmt(res), label
        except Exception as ex:
            return "Ошибка", str(ex)

    def calculate(self):
        if not self.expr:
            return None, None
        orig = self.expr
        try:
            # Преобразуем выражение: приводим функции к нижнему регистру
            expr_to_calc = self.expr
            functions = ["sin", "cos", "tan", "sinh", "cosh", "tanh", "log", "ln", "log2", 
                        "exp", "sqrt", "cbrt", "pow2", "pow10", "abs", "inv", "pct", 
                        "floor", "ceil", "round", "fact", "PI", "E", "PHI"]
            for func in functions:
                expr_to_calc = expr_to_calc.replace(func.upper(), func)
                expr_to_calc = expr_to_calc.replace(func.capitalize(), func)
            
            # Подготавливаем namespace с математическими функциями
            safe_dict = {
                "sin": lambda x: math.sin(self._to_rad(x)) if not self.inv_mode else self._from_rad(math.asin(x)),
                "cos": lambda x: math.cos(self._to_rad(x)) if not self.inv_mode else self._from_rad(math.acos(x)),
                "tan": lambda x: math.tan(self._to_rad(x)) if not self.inv_mode else self._from_rad(math.atan(x)),
                "sinh": lambda x: math.sinh(x) if not self.inv_mode else math.asinh(x),
                "cosh": lambda x: math.cosh(x) if not self.inv_mode else math.acosh(x),
                "tanh": lambda x: math.tanh(x) if not self.inv_mode else math.atanh(x),
                "log": lambda x: math.log10(x) if not self.inv_mode else 10**x,
                "ln": lambda x: math.log(x) if not self.inv_mode else math.exp(x),
                "log2": lambda x: math.log2(x),
                "exp": lambda x: math.exp(x),
                "sqrt": lambda x: math.sqrt(x),
                "cbrt": lambda x: x ** (1/3) if x >= 0 else -((-x) ** (1/3)),
                "pow2": lambda x: x ** 2,
                "pow10": lambda x: 10 ** x,
                "abs": lambda x: abs(x),
                "inv": lambda x: 1 / x,
                "pct": lambda x: x / 100,
                "floor": lambda x: math.floor(x),
                "ceil": lambda x: math.ceil(x),
                "round": lambda x: round(x),
                "fact": lambda x: float(math.factorial(int(x))),
                "PI": math.pi,
                "E": math.e,
                "PHI": (1 + math.sqrt(5)) / 2,
                "__builtins__": {}
            }
            result = eval(expr_to_calc, safe_dict)
            result = float(result)
            if not math.isfinite(result):
                return str(result), orig + " ="
            self._add_history(orig, result)
            self.last_res = result
            self.expr = self._fmt(result)
            self.just_calc = True
            return self._fmt(result), orig + " ="
        except Exception:
            return "Ошибка", orig

    def clear_all(self):
        self.expr = ""; self.last_res = None; self.just_calc = False
        return "0", ""

    def del_last(self):
        self.expr = self.expr[:-1]
        return self.expr or "0"

    def recall_ans(self):
        if self.last_res is not None:
            if self.just_calc:
                self.expr = ""
                self.just_calc = False
            self.expr += self._fmt(self.last_res)
            return self.expr
        return self.expr

    def mem_action(self, act):
        if act == "mc":
            self.memory = 0.0
        elif act == "mr":
            if self.just_calc:
                self.expr = ""; self.just_calc = False
            self.expr += self._fmt(self.memory)
            return self.expr
        elif act in ("m+", "m-"):
            try:
                val = float(eval(self.expr, {"__builtins__": {}}, {})) if self.expr else 0
                self.memory += val if act == "m+" else -val
            except Exception:
                pass
        elif act == "inv":
            return self.input_fn("inv")
        elif act == "floor":
            return self.input_fn("floor")
        self.save_state()
        return self.expr

    def toggle_angle(self):
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        self.save_state()

    def toggle_inv(self):
        self.inv_mode = not self.inv_mode
        self.save_state()

    def _add_history(self, expr_text, result):
        entry = {"expr": expr_text, "val": self._fmt(result)}
        self.history.insert(0, entry)
        if len(self.history) > 50:
            self.history.pop()
        self.save_history()

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except:
                self.history = []

    def save_history(self):
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except:
            pass

    def clear_history(self):
        self.history.clear()
        self.save_history()

    def get_history_items(self):
        return [(entry['expr'], entry['val']) for entry in self.history]

    def recall_history(self, val):
        self.expr = val
        self.just_calc = False
        return val

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
            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.expr = state.get('expr', '')
                    self.last_res = state.get('last_res')
                    self.memory = state.get('memory', 0.0)
                    self.angle_mode = state.get('angle_mode', 'DEG')
                    self.inv_mode = state.get('inv_mode', False)
                    self.just_calc = state.get('just_calc', False)
            except:
                pass