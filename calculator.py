"""The Calculator class ties everything together."""
import math

from .environment import Environment
from .errors import ParseError
from .evaluator import evaluate
from .history import History
from .memory import Memory
from .parser import parse


def format_number(x):
    if isinstance(x, int):
        return str(x)
    if math.isinf(x) or math.isnan(x):
        return str(x)
    if x.is_integer() and abs(x) < 1e15:
        return str(int(x))
    return f"{x:.2f}"


def split_assignment(text):
    """'x = 2 + 3' -> ('x', '2 + 3');  '2 + 3' -> (None, '2 + 3')."""
    if "=" not in text:
        return None, text
    name, _, rest = text.partition("=")
    name = name.strip()
    if not name.isidentifier():
        raise ParseError(f"Invalid assignment target '{name}'")
    return name, rest.strip()


class Calculator:
    def __init__(self, history_size=50):
        self.env = Environment()
        self.memory = Memory()
        self.history = History(history_size)

    def evaluate(self, text):
        text = text.strip()
        if not text:
            raise ParseError("Empty expression")
        target, expression = split_assignment(text)
        value = evaluate(parse(expression), self.env)
        if target is not None:
            self.env.assign(target, value)
        self.env.assign("ans", value)
        self.history.add(text, value)
        return value

    def run(self, text):
        return format_number(self.evaluate(text))

