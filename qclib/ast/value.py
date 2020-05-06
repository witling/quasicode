from .generic import FunctionCall, isof
from ..function import Function

class Value:
    def __init__(self, val):
        self._val = val

    def create(val):
        if isinstance(val, int) or isinstance(val, float):
            return Number(float(val))
        if isinstance(val, bool):
            if val:
                return UzblConstant()
            else:
                op = LogicalNot()
                op.add_arg(UzblConstant())
                return op
        if isinstance(val, str):
            return String(val)
        if isinstance(val, bytes):
            return String(val.decode('utf-8'))
        raise Exception('cannot create value from `{}`'.format(val))

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

class Menge(Value):
    def __init__(self):
        super().__init__({})

    def __getitem__(self, key):
        return self._val[key]

    def __setitem__(self, key, value):
        self._val[key] = value

    def run(self, ctx):
        return self

    def __str__(self):
        return str(self._val)

class Liste(Value):
    def __init__(self):
        super().__init__([])

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

class Access(Ident):
    def __init__(self, parts: list):
        super().__init__(parts[0])
        self._subparts = parts[1:]

    def name(self):
        return self._val

    def subparts(self):
        return self._subparts

    def run(self, ctx):
        val = ctx[self._val]
        assert isof(val, Menge)

        for subpart in self._subparts:
            val = val[subpart]

        return val
