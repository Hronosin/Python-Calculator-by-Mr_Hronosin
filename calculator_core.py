import cmath
import math
import re


def _wrap_real_complex(real_fn, complex_fn):
    def wrapped(value, *args):
        if isinstance(value, complex):
            return complex_fn(value, *args)
        return real_fn(value, *args)
    return wrapped


def sin(value):
    return _wrap_real_complex(math.sin, cmath.sin)(value)


def cos(value):
    return _wrap_real_complex(math.cos, cmath.cos)(value)


def tan(value):
    return _wrap_real_complex(math.tan, cmath.tan)(value)


def asin(value):
    return _wrap_real_complex(math.asin, cmath.asin)(value)


def acos(value):
    return _wrap_real_complex(math.acos, cmath.acos)(value)


def atan(value):
    return _wrap_real_complex(math.atan, cmath.atan)(value)


def sinh(value):
    return _wrap_real_complex(math.sinh, cmath.sinh)(value)


def cosh(value):
    return _wrap_real_complex(math.cosh, cmath.cosh)(value)


def tanh(value):
    return _wrap_real_complex(math.tanh, cmath.tanh)(value)


def sqrt(value):
    if isinstance(value, complex) or (isinstance(value, (int, float)) and value < 0):
        return cmath.sqrt(value)
    return math.sqrt(value)


def log(value, base=math.e):
    if isinstance(value, complex) or isinstance(base, complex):
        return cmath.log(value, base)
    if base == math.e:
        return math.log(value)
    return math.log(value, base)


def ln(value):
    return log(value)


def log10(value):
    if isinstance(value, complex):
        return cmath.log10(value)
    return math.log10(value)


def exp(value):
    if isinstance(value, complex):
        return cmath.exp(value)
    return math.exp(value)


def root(value, degree=2):
    return value ** (1 / degree)


def factorial(value):
    if isinstance(value, complex):
        raise ValueError("Факторіал визначений тільки для натуральних чисел")
    if value != int(value):
        raise ValueError("Факторіал визначений тільки для цілих чисел")
    return math.factorial(int(value))


def deg_to_rad(value):
    return math.radians(value)


def rad_to_deg(value):
    return math.degrees(value)


def km_to_m(value):
    return value * 1000


def m_to_km(value):
    return value / 1000


def mi_to_km(value):
    return value * 1.609344


def km_to_mi(value):
    return value / 1.609344


def c_to_f(value):
    return value * 9 / 5 + 32


def f_to_c(value):
    return (value - 32) * 5 / 9


def c_to_k(value):
    return value + 273.15


def k_to_c(value):
    return value - 273.15

SAFE_NAMESPACE = {
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "asin": asin,
    "acos": acos,
    "atan": atan,
    "sinh": sinh,
    "cosh": cosh,
    "tanh": tanh,
    "sqrt": sqrt,
    "log": log,
    "ln": ln,
    "log10": log10,
    "exp": exp,
    "root": root,
    "factorial": factorial,
    "pi": math.pi,
    "e": math.e,
    "i": 1j,
    "j": 1j,
    "pow": pow,
    "abs": abs,
    "round": round,
    "complex": complex,
    "polar": cmath.polar,
    "rect": cmath.rect,
    "deg_to_rad": deg_to_rad,
    "rad_to_deg": rad_to_deg,
    "km_to_m": km_to_m,
    "m_to_km": m_to_km,
    "mi_to_km": mi_to_km,
    "km_to_mi": km_to_mi,
    "c_to_f": c_to_f,
    "f_to_c": f_to_c,
    "c_to_k": c_to_k,
    "k_to_c": k_to_c,
}


def prepare_expression(expression: str) -> str:
    expression = expression.replace("^", "**")
    expression = re.sub(r"(?P<num>\d+(?:\.\d+)?|\.\d+)\s*i\b", r"\g<num>j", expression)
    expression = re.sub(r"(?<![A-Za-z_0-9])i\b", "1j", expression)
    return expression


def evaluate(expression: str, variables=None):
    expression = prepare_expression(expression).strip()
    if not expression:
        raise ValueError("Порожній вираз")

    env = SAFE_NAMESPACE.copy()
    if variables:
        env.update(variables)

    try:
        return eval(expression, {"__builtins__": None}, env)
    except Exception as error:
        raise ValueError(str(error)) from error
