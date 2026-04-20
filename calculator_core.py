import math

SAFE_NAMESPACE = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "factorial": math.factorial,
    "pi": math.pi,
    "e": math.e,
    "pow": pow,
    "abs": abs,
    "round": round,
}


def prepare_expression(expression: str) -> str:
    return expression.replace("^", "**")


def evaluate(expression: str):
    expression = prepare_expression(expression).strip()
    if not expression:
        raise ValueError("Порожній вираз")

    try:
        return eval(expression, {"__builtins__": None}, SAFE_NAMESPACE)
    except Exception as error:
        raise ValueError(str(error)) from error
