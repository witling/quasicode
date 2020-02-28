from .generic import FunctionCall, isof
from ..program import Function

class Value:
    def __init__(self, val):
        self._val = val

    def create(val):
        if isinstance(val, int) or isinstance(val, float):
            return Number(float(val))
        if isinstance(val, bool) and val:
            return UzblConstant()
        if isinstance(val, str):
            return String(val)
        raise Exception()

    def __str__(self):
        return self._val

    def __int__(self):
        return self._val

    def __float__(self):
        return self._val

    def __bool__(self):
        return bool(self._val)

    def is_assignable(self):
        return False
    
    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, float) or isinstance(other, int):
            return self._val == other
        return self._val == other._val

    def run(self, ctx):
        return self._val

class Constant(Value):
    def __init__(self, val):
        super().__init__(val)

class UzblConstant(Constant):
    def __init__(self):
        super().__init__(True)

    def __str__(self):
        return 'uzbl'

class Number(Value):
    def __init__(self, val):
        super().__init__(val)

    def run(self, ctx):
        return self

    def __str__(self):
        return str(self._val)

class String(Value):
    def __init__(self, val: str):
        super().__init__(val)

class Ident(Value):
    def __init__(self, name: str):
        super().__init__(name)

    def name(self):
        return self._val

    def run(self, ctx):
        val = ctx[self._val]
        # TODO: execute FunctionCall
        if isof(val, Function):
            return FunctionCall(self, []).run(ctx)
        return val
    
    def is_assignable(self):
        return True
